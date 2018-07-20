from .exceptions import AlreadyExistsException
from .exceptions import NotExistsException
from .exceptions import RetriableAPIException
from .exceptions import UnauthorizedException

from os.path import join
import requests
import json


RETRIABLE_STATUS_CODES = (500, 502, 503, 504, 400, 408)
RETRIABLE_EXCEPTIONS = (RetriableAPIException)


class Container:
    def __init__(self, cid, db, client):
        self.id = cid
        self.db = db
        self.client = client

    @property
    def server(self):
        return self.client.server

    @property
    def base_url(self):
        return join(self.server, join(self.db, self.id))

    def create(self, type, id, title=None, path=None):
        """
        path is relative to container url
        """
        path = join(self.base_url, path or '')
        self.client.post_request(
            path,
            data=json.dumps({
                '@type': type,
                'id': id,
                'title': title
            })
        )
        return Resource(path=path, id=id, client=self.client)

    def get(self, target):
        """
        path is relative to container url"""
        path = join(self.base_url, target)
        return Resource(path=path, client=self.client)

    def get_or_create(self, type, id, title=None, path=None):
        try:
            if path:
                target = join(path, id)
            else:
                target = id
            target = target.lstrip(self.base_url)
            return self.get(target)
        except NotExistsException:
            return self.create(type, id, title, path)

    def __getitem__(self, key):
        path = join(self.base_url, key)
        return Resource(path=path, client=self.client)


class ApiClient:
    def __init__(self, server, session, db=None):
        self.server = server
        self.session = session
        self.db = db
        self.container = None

    @property
    def auth_headers(self):
        return {'Authorization': self.session.authorization}

    @property
    def db_url(self):
        if not self.db:
            return None
        return join(self.server, self.db)

    def set_database(self, db):
        self.db = db
        self.container = None

    def list_databases(self):
        return self.get_request(self.server)['databases']

    def list_containers(self, db=None):
        if not db and not self.db:
            raise Exception('Database not specified nor set')
        db_url = join(self.server, db or self.db)
        return self.get_request(db_url)['containers']

    def create_container(self, id, title=None):
        if not self.db:
            raise Exception('Database is not set')
        return self.post_request(self.db_url, data=json.dumps({
            '@type': 'Container',
            'id': id,
            'title': title
        }))

    def set_container(self, cid, db=None):
        if not db and not self.db:
            raise Exception('Database not set')
        self.container = Container(cid, db=db or self.db,
                                   client=self)

    def get_request(self, url, **kwargs):
        if 'include' in kwargs:
            include = kwargs.get('include') or []
            if isinstance(include, list) or isinstance(include, tuple):
                include = f"include={','.join(include)}"
            else:
                include = f"include={include}"
            if '?' in url:
                url = f'{url}&{include}'
            else:
                url = f'{url}?{include}'
        resp = requests.get(url, headers=self.auth_headers, **kwargs)
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 401:
            raise UnauthorizedException
        elif resp.status_code == 404:
            raise NotExistsException
        elif resp.status_code in RETRIABLE_STATUS_CODES:
            raise RetriableAPIException(f'{resp}')
        raise Exception(f'{resp}')

    def post_request(self, url, **kwargs):
        resp = requests.post(url, headers=self.auth_headers, **kwargs)
        if resp.status_code in (200, 201):
            return resp.json()
        elif resp.status_code == 204:
            # Ok but no data returned
            return
        elif resp.status_code == 401:
            raise UnauthorizedException
        elif resp.status_code == 404:
            raise NotExistsException
        elif resp.status_code == 409:
            raise AlreadyExistsException
        elif resp.status_code in RETRIABLE_STATUS_CODES:
            raise RetriableAPIException(f'{resp}')
        raise Exception(f'{resp}')

    def patch_request(self, url, data=None):
        resp = requests.patch(url, headers=self.auth_headers,
                              data=data)
        # Successfully update
        if resp.status_code in range(200, 300):
            return url
        elif resp.status_code == 401:
            raise UnauthorizedException
        elif resp.status_code == 404:
            raise NotExistsException
        elif resp.status_code in RETRIABLE_STATUS_CODES:
            raise RetriableAPIException(f'{resp}')
        raise Exception(f'{resp}')

    def delete_request(self, url, **kwargs):
        resp = requests.delete(url, headers=self.auth_headers, **kwargs)
        if resp.status_code == 200:
            return url
        elif resp.status_code == 401:
            raise UnauthorizedException
        elif resp.status_code == 404 or resp.status_code == 460:
            raise NotExistsException
        elif resp.status_code in RETRIABLE_STATUS_CODES:
            raise RetriableAPIException(f'{resp}')
        raise Exception(f'{resp}')


class Resource:
    def __init__(self, path, client, id=None):
        self.client = client
        if not id:
            id = path.split('/')[-1]
            path = '/'.join(path.split('/')[:-1])
        self.parent_path = path
        self.id = id

    @property
    def path(self):
        return join(self.parent_path, self.id)

    def get(self, target):
        path = join(self.path, target)
        return Resource(path=path, client=self.client)

    def __getitem__(self, key):
        path = join(self.path, key)
        return Resource(path=path, client=self.client)
