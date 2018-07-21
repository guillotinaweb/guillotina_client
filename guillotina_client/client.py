from .api import ApiClient
from .auth import BasicAuth
from .auth import NoAuth
from .auth import JWTAuth


def NoAuthClient(server):
    session = NoAuth()
    return ApiClient(server, session)


def BasicAuthClient(server, username, password):
    session = BasicAuth(username, password)
    return ApiClient(server, session)


def JWTAuthClient(server, container, username, password):
    session = JWTAuth(container, username, password)
    session.login()
    return ApiClient(server, session)
