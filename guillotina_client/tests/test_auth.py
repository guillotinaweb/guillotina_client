from guillotina_client.auth import BasicAuth
from guillotina_client.auth import NoAuth


def test_no_auth():
    auth = NoAuth()
    assert auth.token is None
    assert auth.authorization is None


def test_basic_auth():
    username = 'root'
    password = 'admin'
    auth = BasicAuth(username, password)
    encoded = 'cm9vdDphZG1pbg=='
    assert auth.token == encoded
    assert auth.authorization == f'Basic {encoded}'


def test_jwt_auth(guillotina_server):
    port = guillotina_server
