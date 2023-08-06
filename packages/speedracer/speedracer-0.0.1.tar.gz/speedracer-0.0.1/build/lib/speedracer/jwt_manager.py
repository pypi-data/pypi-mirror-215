"""This module contains classes for conveniently working with JSON Web Tokens (JWTs)

**Example**

```python
manager = JWTManager('https://gateway.com/getjwt')

# get a JWT
token = manager.get()

# get HTTP headers dictionary with an Authorization header set
headers = manager.get_headers()

# get your Common Name
name = manager.get_cn()
```

"""

import datetime
from pathlib import Path
import time
from typing import Optional, Union, Tuple, Dict

import jwt
import requests

class JWTManager:
    """A class for getting JSON Web Tokens. Handles refreshing."""
    def __init__(self, url:str, cert:Tuple[str, str]=(Path.home().joinpath('cert.crt'),
            Path.home().joinpath('cert.key')),
            verify:Union[str, bool]=True) -> None:
        '''Create a JWT Manager

        Arguments:
            url: The URL of the API Gateway to fetch JWTs from
            cert: A Tuple containing the paths to the certificate and
                key to use with the API Gateway. By default, looks in the
                user's home directory for the files cert.crt and cert.key
            verify: A bool or a path to a Certificate Authority. Passed to the requests library
        '''
        self.token:Optional[Union[str, None]] = None
        '''The most recently fetched JWT. Use the `get` method instead of accessing this directly'''
        self.url:str = url
        '''The URL of the API Gateway to fetch JWTs from'''
        self.cert:Tuple[str, str] = cert
        '''A Tuple containing the paths to the certificate and key to use with the API Gateway'''
        self.verify:Union[str, bool] = verify
        '''A bool or a path to a Certificate Authority. Passed to the requests library'''

    def __is_expired(self) -> None:
        in_five_minutes = time.mktime(
            (datetime.datetime.utcnow() + datetime.timedelta(minutes=5)).timetuple())
        claims = jwt.decode(self.token, options={'verify_signature': False})
        if 'exp' in claims:
            return claims['exp'] < in_five_minutes
        return False

    def __get_jwt(self) -> None:
        resp = requests.get(self.url, cert=self.cert, verify=self.verify, timeout=10)
        self.token = resp.text.strip()

    def get(self) -> str:
        '''Returns a cached JWT or a new one if the cached JWT is close to expiration

        Example:
            ```
            token = manager.get()
            ```

        Returns:
            str: JWT
        '''
        if self.token is None or self.__is_expired():
            self.__get_jwt()
        return self.token

    def get_headers(self) -> Dict:
        '''Returns a Dict containing an Authorization HTTP header for use with Autobahn APIs

        Example:

            ```
            headers = manager.get_headers()
            ```

        Returns:
            Dict: contains Authorization header

                {
                    'Authorization': 'Bearer <jwt-here>'
                }
        '''
        return {
            'Authorization': 'Bearer ' + self.get()
        }

    def get_cn(self) -> str:
        '''Extracts the CN claim from a JSON Web Token

        Example:
            ```
            name = manager.get_cn()
            ```

        Returns:
            str: common name extracted from the JWT
        '''
        return jwt.decode(self.get(), options={'verify_signature': False})['CN']
