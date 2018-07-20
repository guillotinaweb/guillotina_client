from guillotina_client.swagger import EndpointProducer
import os

import pytest
import logging


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
