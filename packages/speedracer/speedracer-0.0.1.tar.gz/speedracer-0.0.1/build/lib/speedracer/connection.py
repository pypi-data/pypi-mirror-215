'''This module contains classes for subscribing

**Example**

```python

    conn = Connection('https://account-server.com')
    sub = await conn.subscribe('mydata')
    async for msg in sub:
        print(msg.data.decode())

```
'''

import asyncio
import datetime
import hashlib
from pathlib import Path
import ssl
from enum import Enum
from typing import Union, Optional, Callable, Tuple, List, Dict, Iterable
from urllib.parse import urlparse, urlunparse

import requests
import nats
from nats.errors import TimeoutError as NatsTimeoutError

from.jwt_manager import JWTManager

class Offset(str, Enum):
    '''The offset to start consuming messages from'''
    BEGIN = 'begin'
    NOW = 'now'

class Connection:
    '''This class holds information for connection to the Mission Data Broker (MDB)'''
    def __init__(self, url:str, cert:Tuple[str, str]=(Path.home().joinpath('cert.crt'),
                Path.home().joinpath('cert.key')),
            ca_bundle:Optional[str]=None) -> None:
        '''Create a Connection

        Example:
            ```
            conn = Connection('https://mdb-account-server.com')
            ```

        Arguments:
          url: Base URL of the MDB Acccount Server (MAS)
          cert: A Tuple containing the paths to the certificate and
            key to use with the API Gateway. By default, looks in the
            user's home directory for the files cert.crt and cert.key
          ca_bundle: A path to a Certificate Authority
        '''
        def get_urls():
            config_url = urlparse(url)
            config_url = urlunparse(config_url._replace(path='/api/v1/config'))
            return requests.get(config_url, verify=self.verify, timeout=10).json()

        self.cert: Tuple[str, str] = cert
        '''Certificate path, key path Tuple. Default looks for cert.crt and
        cert.key in user's home directory'''
        self.ca_bundle: Optional[str] = ca_bundle
        '''Path to Certificate Authority'''
        self.verify: Union[str, bool] = ca_bundle if ca_bundle else True
        '''Used by requests. Set to value self.ca_bundle if set and True otherwise'''
        self.urls: Dict = get_urls()
        '''A dict containing URLs to services'''
        self.jwt_manager: JWTManager = JWTManager(self.urls['api_gateway_url'],
                cert=cert, verify=self.verify)
        '''A `JWTManager` for authenticating to the MDB'''
        self.subscriptions: List = []
        '''An array of all Subscriptions associated with this Connection'''

    async def subscribe(self, dataset:str, offset:Offset=Offset.BEGIN, batch_size:int=10,
            callback:Optional[Callable]=None) -> Iterable:
        '''Subscribe to a data stream. Returns a Subscription which is an Iterable

        Example:
            ```
            sub = await conn.subscribe('mydataset')
            async for msg in sub:
                print(msg.data.decode())
            ```

        Arguments:
            dataset: The slug of the dataset to subscribe to
            offset: The offset to start consuming messages from
            batch_size: The number of messages the client will
                pull at a time
        '''
        sub = self.Subscription(self.urls, self.jwt_manager, self.ca_bundle,
                dataset, offset, batch_size, callback)
        await sub.start()
        self.subscriptions.append(sub)
        return sub

    async def close(self):
        '''Close all subscriptions associated with this Connection'''

        # pylint: disable=broad-exception-caught
        # Try closing each subscription

        for sub in self.subscriptions:
            try:
                await sub.close()
            except Exception as ex:
                print('exception closing subscription:', ex)
            self.subscriptions = []


    class Subscription:
        '''This class is a subscription to a data stream. Iterable'''

        # pylint: disable=too-many-instance-attributes
        # Seven attributes is not enough

        # pylint: disable=too-many-arguments
        # Only called internally so it is fine

        def __init__(self, urls:Dict, jwt_manager:JWTManager, ca_bundle:Optional[str],
                dataset:str, offset:Offset, batch_size:int, callback:Optional[Callable]) -> None:
            '''Create a subscription. Use a Connection's `subscribe` method instead

            Arguments:
                urls: A Dict containing URLs to services
                jwt_manager: A `JWTManager` for authenticating to the MDB
                ca_bundle: Path to a Certificate Authority
                dataset: The slug of the dataset to subscribe to
                offset: The offset to start consuming messages from
                batch_size: The number of messages the client will pull
                    at a time
                callback: A Callable that takes a NATS message as an
                    argument. Called for each messages received
            '''
            self.verify:Union[str, bool] = ca_bundle if ca_bundle else True
            '''Used by requests. Set to value of ca_bundle if set and True otherwise'''
            self.urls:Dict = urls
            '''A Dict containing URLs to services'''
            self.jwt_manager:JWTManager = jwt_manager
            '''A JWTManager for authenticating to the MDB'''
            self.dataset:str = dataset
            '''The dataset slug for this subscription'''
            self.offset:Offset = offset
            '''The offset to start consuming messages from'''
            self.batch_size:int = batch_size
            '''Number of messages the subscription will pull at a time'''
            self.callback:Optional[Callable] = callback
            '''Optional callback that takes a NATS message as an argument'''
            self.__ssl_context:ssl.SSLContext = ssl.create_default_context()
            '''SSL context used by aiohttp'''
            if ca_bundle:
                self.__ssl_context.load_verify_locations(ca_bundle)
            self.__nats_conn = None
            '''NATS Connection'''
            self.__js_ctx = None
            '''NATS JetStream Context'''
            self.__psub = None
            '''NATS Pull Subscription'''
            self.__consumer_name:str = None
            '''NATS Consumer name'''
            self.__cb_task = None
            '''Asyncio Task for message callback'''

            def get_subject() -> str:
                headers = jwt_manager.get_headers()
                headers['Accept'] = 'application/vnd.pgrst.object+json'
                resp = requests.get(
                        f"{urls['registry_url']}/api/v1/datasets?slug=eq.{self.dataset}",
                        headers=headers, verify=self.verify, timeout=10)
                dataset_entry = resp.json()
                subject = f"EVENTS.{self.dataset}"
                if dataset_entry.get('data_object_backend'):
                    if dataset_entry['data_object_backend'] == 'MDB':
                        subject = f"OBJECTS.{self.dataset}"
                elif dataset_entry.get('mdb_object_publish'):
                    if dataset_entry['data_object_backend']:
                        subject = f"OBJECTS.{self.dataset}"
                return subject

            self.subject: str = get_subject()
            '''NATS Subject'''

        async def __aiter__(self):
            while True:
                try:
                    msgs = await self.__psub.fetch(self.batch_size)
                    for msg in msgs:
                        await msg.ack()
                    for msg in msgs:
                        yield msg
                except NatsTimeoutError: # no messages to return yet
                    pass
                except KeyboardInterrupt:
                    break

        async def __call_callback(self):
            async for msg in self:
                self.callback(msg)

        async def start(self):
            '''Start the Subscription. This is called automatically
            when using `Connection.subscribe()`'''
            def signature(_):
                return bytes('', 'UTF-8')

            def get_mas_jwt() -> bytearray:
                resp = requests.get(f"{self.urls['mas_url']}/api/v1/user/jwt/{self.dataset}",
                        headers=self.jwt_manager.get_headers(), verify=self.verify, timeout=10)
                encoded_token = resp.text.encode()
                return bytearray(encoded_token)

            def get_consumer_name() -> str:
                cn_hash = hashlib.md5(self.jwt_manager.get_cn().encode())
                return cn_hash.hexdigest()[:-1] + '0'


            async def create_conn() -> None:
                self.__nats_conn = await nats.connect(
                        self.urls['nats_websocket_url'],
                        name=f"{self.jwt_manager.get_cn()} ({self.dataset})",
                        signature_cb=signature,
                        user_jwt_cb=get_mas_jwt,
                        tls=self.__ssl_context)
                self.__js_ctx = self.__nats_conn.jetstream()
                self.__consumer_name = get_consumer_name()

            await create_conn()
            await self.__create_sub()

        async def __create_sub(self, start_sequence:Union[int, None]=None,
                start_datetime:Union[datetime.datetime, None]=None) -> None:

            cfg=nats.js.api.ConsumerConfig(inactive_threshold=60.0*60.0*24.0*7.0) # seconds

            if start_sequence is not None:
                cfg.deliver_policy = (
                    nats.js.api.DeliverPolicy.BY_START_SEQUENCE)
                cfg.opt_start_seq = start_sequence
            elif start_datetime is not None:
                cfg.deliver_policy = (
                    nats.js.api.DeliverPolicy.BY_START_TIME)
                cfg.opt_start_time =  start_datetime.replace(
                        tzinfo=datetime.timezone.utc).isoformat()
            elif self.offset == 'new':
                cfg.deliver_policy = nats.js.api.DeliverPolicy.NEW
            else:
                cfg.deliver_policy = nats.js.api.DeliverPolicy.ALL

            self.__psub = await self.__js_ctx.pull_subscribe(
                    subject=self.subject,
                    durable=self.__consumer_name,
                    config=cfg)

            if self.callback and not self.__cb_task:
                self.__cb_task = asyncio.create_task(self.__call_callback())

        async def seek(self, start_sequence=None, start_datetime=None) -> None:
            '''Move cursor to specified sequence number or datetime

            Example:
                ```
                await sub.seek(start_sequence=1)
                await sub.seek(start_datetime=datetime.datetime.utcnow() - datetime.timedelta(minutes=5))
                ```

            Arguments:
                start_sequence: The sequence number of the message to seek to
                start_datetime: The datetime to seek to
            '''
            if start_sequence is None and start_datetime is None:
                return
            await self.__psub.unsubscribe()
            await self.__delete_consumer()
            await self.__create_sub(start_sequence, start_datetime)

        async def __delete_consumer(self) -> bool:
            stream_name = self.subject.replace('.', '_')
            return await self.__js_ctx.delete_consumer(stream_name, self.__consumer_name)

        async def wait(self, messages:Union[int, None]=None,
                timeout:Union[int, datetime.datetime, datetime.timedelta, None]=None) -> None:
            '''Block until specified number of messages consumed
            and specified amount of time has elapsed

            Example:
                ```
                await sub.wait(messages=15)
                await sub.wait(timeout=5)
                ```

            Arguments:
                messages: The number of messages to wait for
                timeout: The number of seconds to wait for, the
                    datetime to wait until, or the timedelta to
                    wait for
            '''
            if messages:
                msgs_target = self.__psub.delivered + messages
                while self.__psub.delivered < msgs_target:
                    await asyncio.sleep(1)
            if timeout:
                if isinstance(timeout, datetime.datetime):
                    await asyncio.sleep((timeout - datetime.datetime.utcnow()).total_seconds())
                elif isinstance(timeout, datetime.timedelta):
                    await asyncio.sleep(timeout.total_seconds())
                else:
                    await asyncio.sleep(timeout)

        async def close(self) -> None:
            '''Close this Subscription'''
            if self.__cb_task:
                self.__cb_task.cancel()
                await asyncio.sleep(0.1)
            await self.__nats_conn.close()
