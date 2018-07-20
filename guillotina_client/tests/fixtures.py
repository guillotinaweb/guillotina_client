from guillotina_client.swagger import EndpointProducer
from guillotina_client.client import GuillotinaClient
from aiohttp.test_utils import TestServer

from guillotina.tests.fixtures import GuillotinaDBRequester

import logging
import os
import pytest
import threading
import asyncio


@pytest.fixture(scope='function')
def guillotina_server(db, guillotina_main, loop):
    server = TestServer(guillotina_main)

    requester = GuillotinaDBRequester(server=server, loop=loop)

    def loop_in_thread(loop, server):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(server.start_server(loop=loop))

    t = threading.Thread(target=loop_in_thread, args=(loop, server,))
    t.daemon = True
    t.start()

    # Wait for server port assignment
    import time
    time.sleep(0.2)

    yield requester
    #    loop.run_until_complete(server.close())


@pytest.fixture(scope='function')
def client(guillotina_server):
    host = guillotina_server.server.host
    port = guillotina_server.server.port
    server_url = f'http://{host}:{port}'
    yield GuillotinaClient(server_url, 'root', 'root')


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
