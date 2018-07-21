from guillotina_client.auth import BasicAuth
from guillotina_client.auth import JWTAuth
from guillotina_client.auth import NoAuth
from guillotina_client.tests.fixtures import TEST_USER_NAME, TEST_USER_PWD
from os.path import join
import time


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
    container = join(guillotina_server, 'db/guillotina')
    session = JWTAuth(container, TEST_USER_NAME, TEST_USER_PWD)
    session.login()
    assert session.token is not None
    assert not session.token_expired

    # Check only refreshed if expired or force=True
    old_token = session.token
    session.refresh_token(force=False)
    assert session._token == old_token

    # Wait for server to process request
    time.sleep(1)

    # Check force works
    session.refresh_token(force=True)
    assert session._token != old_token

    # Wait for server to process request
    time.sleep(1)

    # Check that they get refreshed when expired
    session._expires = 00
    assert session.token_expired is True
    session.refresh_token(force=False)
    assert session._token != old_token
