def test_endpoint_name(endpoint_object):
    assert endpoint_object.endpoint == "@behaviors"


def test_endpoint_summary(endpoint_object):
    assert endpoint_object.summary == {
        'patch': 'Add behavior to resource',
        'delete': 'Remove behavior from resource',
        'get': 'Get information on behaviors for this resource'
    }


def test_endpoint_methods(endpoint_object):
    assert endpoint_object.methods == ['patch', 'delete', 'get']


def test_endpoint_responses(endpoint_object):
    assert endpoint_object.responses == {
        'delete': {
            '200': {'description': 'Successfully removed behavior'},
            '201': {'description': 'Behavior not assigned here'}},
        'get': {
            '200': {'description': 'A listing of behaviors for content',
                    'schema': {'$ref': '#/definitions/BehaviorsResponse'}}},
        'patch': {
            '200': {'description': 'Successfully added behavior'},
            '201': {'description': 'Behavior already assigned here'}}}


def test_endpoint_path(endpoint_object):
    assert endpoint_object.path == '/db/account3/folder/@behaviors'


def test_endpoint_parameters(endpoint_object):
    assert endpoint_object.parameters == {
        'delete': [{'in': 'body',
                    'name': 'body',
                    'schema': {'$ref': '#/definitions/Behavior'}}],
        'get': {},
        'patch': [{'in': 'body',
                   'name': 'body',
                   'schema': {'$ref': '#/definitions/Behavior'}}]}
