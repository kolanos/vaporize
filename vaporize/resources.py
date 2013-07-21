# -*- coding: utf-8 -*-

import json


from .core import handle_request, query
from .utils import dotdict


class Resource(dotdict):
    """Base class for a resource."""

    BASE_URL = None
    SERVICE = None
    IDENTIFIER = 'name'

    def __init__(self, *args, **kwargs):
        if self.SERVICE is not None:
            self.BASE_URL = '/'.join([get_url(self.SERVICE), self.plural])
        super(Resource, self).__init__(*args, **kwargs)

    def __repr__(self):
        if self.IDENTIFIER:
            if isinstance(self.IDENTIFIER, list):
                for i in self.IDENTIFIER:
                    if self.get(i):
                        self.IDENTIFIER = i
                        break
                else:
                    self.IDENTIFIER = None
            if self.IDENTIFIER and self.IDENTIFIER in self:
                return '<%s %s>' % (self.__class__,
                                    self.get(self.IDENTIFIER))
        return super(Resource, self).__repr__()

    @property
    def singular(self):
        return underscore(self.__class__)

    @property
    def plural(self):
        return pluralize(underscore(self.__class__))


class CloudBlockStorage(Resource):
    SERVICE = 'cloudblockstorage'


class CloudDatabase(Resource):
    SERVER = 'clouddatabases'


class CloudDNS(Resource):
    SERVER = 'clouddns'


class CloudLoadBalancer(Resource):
    SERVICE = 'cloudloadbalancers'


class CloudServer(Resource):
    SERVICE = 'cloudservers'


class CloudServerOpenStack(Resource):cloudserversopenstack
    SERVICE = 'cloudserversopenstack'


class Createable(object):
    """Add a create() method to a resource."""

    @classmethod
    def create(cls, data):
        """Create an object."""
        data = json.dumps(data)
        return handle_request('post', cls.BASE_URL, data, cls, cls.singular)


class Modifyable(object):
    """Add modify() method to resources."""

    def modify(self, data):
        assert 'id' in self, 'Missing id attribute.'
        data = json.dumps(data)
        url = '/'.join([self.BASE_URL, str(self.id)])
        handle_request('put', url, data=data)


class Findable(object):
    """Adds a find method to a reosource."""

    @classmethod
    def find(cls, id):
        """Returns an object by ``id``.

        :param id: The ``id`` of the object to retrieve.
        :type id: int or str
        :returns: An object matching the ``id``.
        :rtype: :class:`Resource`

        .. versionadded:: 0.4
        """
        url = '/'.join([cls.BASE_URL, str(id)])
        return handle_request('get', url, wrapper=cls,
                              container=cls.singular)


class Deleteable(object):
    """Adds a delete method to a resource."""

    def delete(self):
        """Delete this object.

        .. versionadded:: 0.4
        """
        assert 'id' in self, 'Missing id attribute.'
        url = '/'.join([self.BASE_URL, str(self['id'])])
        handle_request('delete', url)


class Listable(object):
    """Adds a list() method to a resource."""

    @classmethod
    def list(cls, limit=None, offset=None, detail=False):
        """Returns a list of objects.

        :param limit: Limit the result set by a cetain number.
        :type limit: int
        :param offset: Offset the result set by a certain number.
        :type offset: int
        :param detail: Return additional details about each object.
        :type detail: bool
        :returns: A list of objects.
        :rtype: A list of :class:`Resource`

        .. versionadded:: 0.4
        """
        url = [cls.BASE_URL]
        if detail:
            url.append('detail')
        url = '/'.join(url)
        if limit is not None or offset is not None:
            url = query(url, limit=limit, offset=offset)
        return handle_request('get', url, wrapper=cls,
                              container=cls.plural)


class Reloadable(object):
    """adds a reload() method to a resource."""

    def reload(self):
        """Reload this object.

        :returns: An updated object.
        :rtype: :class:`Resource`

        .. versionadded:: 0.4
        """
        assert 'id' in self, 'Missing id attribute.'
        response = self.find(self.id)
        self.update(response)
        return self
