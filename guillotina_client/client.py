from .api import ApiClient
from .auth import BasicAuth


def GuillotinaClient(server, username, password, auth_type='basic'):
    if auth_type != 'basic':
        raise Exception(f'Auth type not supported {auth_type}')
    session = BasicAuth(username, password)
    return ApiClient(server, session)
