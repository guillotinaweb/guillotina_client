from guillotina_client.swagger import EndpointProducer
from guillotina_client.client import BasicAuthClient
from aiohttp.test_utils import TestServer
from guillotina.tests.fixtures import get_db_settings
from guillotina.component import globalregistry
from guillotina.content import load_cached_schema
from guillotina.factory import make_app
from aiohttp.test_utils import unused_port
from multiprocessing import Process
from guillotina_client.auth import BasicAuth
import logging
import os
from os.path import join
import pytest
import asyncio
import time
import requests

from guillotina.testing import TESTING_SETTINGS


TESTING_SETTINGS.setdefault('applications', [])
TESTING_SETTINGS['applications'].append('guillotina_dbusers')
TESTING_SETTINGS['applications'].append('guillotina_swagger')

TESTING_ROOT_USER = 'root'
TESTING_ROOT_PWD = 'admin'
TEST_USER_NAME = 'testuser'
TEST_USER_PWD = 'password'
TEST_USER_EMAIL = 'test@user.com'


def guillotina_in_thread(port):
    # Create a new loop and set it
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # Create guillotina app
    globalregistry.reset()
    aioapp = make_app(settings=get_db_settings(), loop=loop)
    aioapp.config.execute_actions()
    load_cached_schema()
    # Create test server with app
    server = TestServer(aioapp, loop=loop, port=port)
    loop.run_until_complete(server.start_server(loop=loop))
    loop.run_forever()


@pytest.fixture(scope='function')
def guillotina_server():
    """Starts a guillotina server in a separate thread
    """
    # Choose random port
    port = unused_port()
    # Start new thread that launches guillotina server
    p = Process(target=guillotina_in_thread, args=(port,))
    p.start()
    # Wait a bit until the server is started

    time.sleep(2.5)

    # Yield port so that client knows where to connect
    guillotina_url = f'http://localhost:{port}'
    print(f'\n*** Server running at {guillotina_url}')
    # Populate with initial data
    populate_server(guillotina_url)
    yield guillotina_url
    # Tead-down code
    p.terminate()


@pytest.fixture(scope='function')
def client(guillotina_server):
    client = BasicAuthClient(guillotina_server, 'root', 'admin')
    yield client


def populate_server(guillotina_url):
    basic = BasicAuth(TESTING_ROOT_USER, TESTING_ROOT_PWD)
    auth_headers = {'Authorization': basic.authorization}
    base_url = join(guillotina_url, 'db')
    # Create default container
    resp = requests.post(
        base_url,
        headers=auth_headers,
        json={'@type': 'Container', 'id': 'guillotina'}
    )
    assert resp.status_code == 200
    container_url = join(base_url, 'guillotina')
    # Install dbusers addon
    resp = requests.post(
        join(container_url, '@addons'),
        headers=auth_headers,
        json={'id': 'dbusers'}
    )
    assert resp.status_code == 200
    # Add the test user
    resp = requests.post(
        join(container_url, 'users'),
        headers=auth_headers,
        json={'@type': 'User',
              'username': TEST_USER_NAME,
              'email': TEST_USER_EMAIL,
              'password': TEST_USER_PWD}
    )
    assert resp.status_code == 201


@pytest.fixture(scope='function')
def logger():
    return logging.getLogger('Swagger Logger mockup')


@pytest.fixture(scope='function')
def swagger_mock():
    script_dir = os.path.dirname(__file__)
    rel_path = "./swagger_response.json"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, 'r') as infile:
        swagger_mock = infile.read()
    return swagger_mock


@pytest.fixture(scope='function')
def endpoint_object(logger, swagger_mock):
    endpoint_producer = EndpointProducer(swagger_mock, logger)
    return next(endpoint_producer.endpoint_generator())
