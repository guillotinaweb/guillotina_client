from .exceptions import RefreshTokenFailedException
from .exceptions import LoginFailedException
from datetime import datetime
from base64 import b64encode
import requests


class IAuth:
    """
    Defines the auth interface
    """
    @property
    def token(self):
        pass

    @property
    def authorization(self):
        pass

    def login(self, **kwargs):
        return None

    def refresh_token(self, **kwargs):
        return None


class NoAuth(IAuth):
    @property
    def token(self):
        return None

    @property
    def authorization(self):
        return None


class BasicAuth(IAuth):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def token(self):
        return b64encode(f'{self.username}:{self.password}'.encode()).decode()

    @property
    def authorization(self):
        return f'Basic {self.token}'


class JWTAuth(IAuth):
    def __init__(self, container, username, password):
        self.container = container
        self.username = username
        self.password = password
        self._token = None
        self._expires = None

    @property
    def token(self):
        return self._token

    @property
    def token_expired(self):
        now = datetime.utcnow().timestamp()
        return now > self._expires

    @property
    def authorization(self):
        return f'Bearer {self.token}'

    def login(self, **kwargs):
        response = requests.post(
            join(self.container, '@login'),
            json={
                'username': self.username,
                'password': self.password
            }
        )
        if response.status_code != 200:
            raise LoginFailedException

        resp = response.json()
        self._token = resp['token']
        self._expires = resp['exp']

    def refresh_token(self, **kwargs):
        force = kwargs.get('force') or False
        if self.token_expired or force:
            response = requests.post(
                join(self.container, '@refresh_token'),
                json={
                    'username': self.username,
                    'password': self.password
                }
            )
            if response.status_code != 200:
                raise RefreshTokenFailedException

            resp = response.json()
            self._token = resp['token']
            self._expires = resp['exp']
