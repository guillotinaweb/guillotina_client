from guillotina_client.auth import BasicAuth


def test_basic_auth():
    username = 'root'
    password = 'admin'
    auth = BasicAuth(username, password)
    encoded = 'cm9vdDphZG1pbg=='
    assert auth.token == encoded
    assert 'Authorization' in auth.authorization
    assert auth.authorization['Authorization'] == f'Basic {encoded}'
