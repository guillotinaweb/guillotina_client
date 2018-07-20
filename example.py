from guillotinaclient import GuillotinaClient
from guillotinaclient.api import Resource
from guillotinaclient.exceptions import AlreadyExistsException
import random


# You can instantiate a client by giving the server credentials
g = GuillotinaClient('http://localhost:8080', 'root', 'root')

# Get a map of databases and containers
containers_per_db = {}
for db in g.list_databases():
    for c in g.list_containers(db):
        containers_per_db.setdefault(db, [])
        containers_per_db[db].append(c)

# Test db and container
db = 'db'
cid = 'container9w29'

# First set the database
g.set_database(db)

# You can create a container it it doesn't exist already
try:
    g.create_container(id=cid, title='My Container')
except AlreadyExistsException:
    pass
finally:
    # Then set the client to use that container, so you can access it
    # later
    g.set_container(cid, db=db)

# Once you set the container, you can create content
folder = g.container.get_or_create(
    type='Folder',
    id='folder1',
    title='My Folder'
)

folder2 = g.container.get_or_create(
    type='Folder',
    id='folder2',
    path=folder.path
)

# Or just with dict-like access
folder1 = g.container['folder1']

# You can create items within a folder too
item = g.container.get_or_create(
    type='Item',
    id='myitem',
    title='My Item',
    path=folder.path
)

# We can also access nested contents
folder2 = g.container['folder1']['folder2']
myitem = g.container['folder1']['myitem']
assert myitem.id == item.id
