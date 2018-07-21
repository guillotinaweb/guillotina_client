from guillotina_client.swagger import EndpointProducer
from guillotina_client.client import GuillotinaClient
from aiohttp.test_utils import TestServer
from guillotina.tests.fixtures import get_db_settings
from guillotina.component import globalregistry
from guillotina.content import load_cached_schema
from guillotina.factory import make_app
from aiohttp.test_utils import unused_port
from multiprocessing import Process
import logging
import os
import pytest
import asyncio
import time


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
    time.sleep(0.5)

    # Yield port so that client knows where to connect
    yield port
    p.terminate()


@pytest.fixture(scope='function')
def client(guillotina_server):
    port = guillotina_server
    server_url = f'http://localhost:{port}'
    print(f'*** Server running at {server_url}')
    yield GuillotinaClient(server_url, 'root', 'admin')


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
