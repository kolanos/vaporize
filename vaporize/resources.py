# -*- coding: utf-8 -*-

import json


from vaporize.core import get_url, handle_request, query
from vaporize.utils import dotdict


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


class CloudServerOpenStack(Resource):
    SERVICE = 'cloudserversopenstack'


class Createable(dotdict):
    """Add a create() method to a resource."""

    @classmethod
    def create(cls, data):
        """Create an object.

        This method will be overloaded.

        :param data: Dictionary of key/values to create.
        :type data: dict
        :returns: A newly created object.
        :rtype: :class:`Resource`

        .. versionadded:: 0.4
        """
        data = json.dumps(data)
        return handle_request('post', cls.BASE_URL, data, cls, cls.singular)


class Modifyable(dotdict):
    """Add modify() method to resources."""

    def modify(self, data):
        """Modify an object.

        This method will be overloaded.

        :param data: Dictionary of key/values to modify.
        :type data: dict

        .. versionadded:: 0.4
        """
        assert 'id' in self, 'Missing id attribute.'
        data = json.dumps(data)
        url = '/'.join([self.BASE_URL, str(self.id)])
        handle_request('put', url, data=data)


class Findable(dotdict):
    """Adds a find() method to a reosource."""

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


class Deleteable(dotdict):
    """Adds a delete() method to a resource."""

    def delete(self):
        """Delete this object.

        .. versionadded:: 0.4
        """
        assert 'id' in self, 'Missing id attribute.'
        url = '/'.join([self.BASE_URL, str(self['id'])])
        handle_request('delete', url)


class Listable(dotdict):
    """Adds a list() method to a resource."""

    @classmethod
    def list(cls, **params):
        """Returns a list of objects.

        :param params: Query parameters, such as ``limit`` or ``offset``.
        :type params: dict
        :returns: A list of objects.
        :rtype: A list of :class:`Resource`.

        .. versionadded:: 0.4
        """
        url = [cls.BASE_URL]
        if 'detail' in params:
            params.pop('detail')
            url.append('detail')
        url = '/'.join(url)
        url = query(url, **params)
        return handle_request('get', url, wrapper=cls,
                              container=cls.plural)


class Reloadable(dotdict):
    """Adds a reload() method to a resource."""

    def reload(self):
        """Reload this object.

        :returns: An updated object.
        :rtype: :class:`Resource`

        .. versionadded:: 0.4
        """
        assert 'id' in self, 'Missing id attribute.'
        response = self.find(self.id)
        self.update(**response)
        return self
