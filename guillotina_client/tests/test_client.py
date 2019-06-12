import pytest

from guillotina_client.exceptions import (
    NotExistsException, AlreadyExistsException
)


def test_client_basic(client):
    # Test container id
    cid = 'guillotina'

    # Set test container
    client.set_container(cid, db='db')
    resp = client.get_request(client.container.base_url)
    assert client.container.id == cid == resp['@name']
    # container does not exists, raise exception
    with pytest.raises(NotExistsException):
        client.set_container(cid, db='db-custom')
    client.create_container(cid, db="db-custom")
    client.set_container(cid, db='db-custom')
    with pytest.raises(AlreadyExistsException):
        client.create_container(cid, db="db-custom")
    # Get a map of databases and containers
    containers_per_db = {}
    for db in client.list_databases():
        for c in client.list_containers(db):
            containers_per_db.setdefault(db, [])
            containers_per_db[db].append(c)
        assert containers_per_db[db] == [cid]
    # Once you set the container, you can create content
    folder = client.container.get_or_create(
        type='Folder',
        id='folder',
        title='My Folder'
    )
    # Create a subfoder
    subfolder = client.container.get_or_create(
        type='Folder',
        id='subfolder',
        path=folder.path
    )

    # You can create items within a folder too
    item = client.container.get_or_create(
        type='Item',
        id='myitem',
        title='My Item',
        path=folder.path
    )
    subitem = client.container.get_or_create(
        type='Item',
        id='myitem',
        title='My Item',
        path=subfolder.path
    )

    # We can also access nested contents
    # Or just with dict-like access
    folder_ = client.container['folder']
    item_ = folder_['myitem']
    subfolder_ = folder_['subfolder']
    subitem_ = subfolder_['myitem']
    assert '@sharing' in subitem.list_endpoints
    assert '@sharing' in folder.list_endpoints
    assert '@sharing' in item.list_endpoints
    # Check that dynamic methods are created
    assert 'getsharing' in dir(item) and callable(item.getsharing)
    assert 'getsharing' in dir(folder) and callable(item.getsharing)
    assert 'getsharing' in dir(subitem) and callable(item.getsharing)
    assert folder.path == folder_.path
    assert subfolder.path == subfolder_.path
    assert item.path == item_.path
    assert subitem.path == subitem_.path
