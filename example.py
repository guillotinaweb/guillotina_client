from guillotinaclient import GuillotinaClient
from guillotinaclient.api import Resource
from guillotinaclient.exceptions import AlreadyExistsException
import random


# You can instantiate a client by giving the server credentials
g = GuillotinaClient('http://localhost:8080', 'root', 'root')
