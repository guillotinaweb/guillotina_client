def test_client_basic(client):
    # Test container id
    cid = 'guillotina'

    # Set test container
    client.set_container(cid, db='db')

    resp = client.get_request(client.container.base_url)
    assert client.container.id == cid == resp['@name']

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

    assert folder.path == folder_.path
    assert subfolder.path == subfolder_.path
    assert item.path == item_.path
    assert subitem.path == subitem_.path
