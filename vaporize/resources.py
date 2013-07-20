# -*- coding: utf-8 -*-

import json

from .core import handle_request, query
from .utils import camelcase_to_underscore


class Resource(dict):
    """
    Base class for a resource.

    Give dict support for dot notation and force value changes through
    __setitem__ so that it can be overloaded/overidden.
    """

    BASE_URL = None
    CONTAINER = None
    IDENTIFIER = ['id', 'name']

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def __repr__(self):
        if self.IDENTIFIER:
            if isinstance(self.IDENTIFIER, list):
                for i in self.IDENTIFIER:
                    if self.get(i):
                        self.IDENTIFIER = i
                        break
            if self.IDENTIFIER in self:
                return '<%s %s>' % (self.__class__,
                                    self.get(self.IDENTIFIER))
        return super(Resource, self).__repr__()


    def update(self, *args, **kwargs):
        if len(args) > 1:
            raise TypeError("update expected at most 1 arguments, got %d" % len(args))
        other = dict(*args, **kwargs)
        for key in other:
            self[key] = other[key]

    def setdefault(self, key, value=None):
        if key not in self:
            self[key] = value
        return self[key]

    def __setitem__(self, key,value):
        key = camelcase_to_underscore(key)
        super(Resource, self).__setitem__(key, value)

    __setattr__ = __setitem__
    __getattr__ = dict.__getitem__
    __delattr__ = dict.__delitem__


class CreateableResource(object):
    """Add a create() method to a resource."""

    @classmethod
    def create(cls, data):
        """Create an object."""
        data = json.dumps(data)
        return handle_request('post', cls.BASE_URL, data, cls, 'image')


class FindableResource(object):
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
                              container=cls.CONTAINER)


class DeleteableResource(object):
    """Adds a delete method to a resource."""

    def delete(self):
        """Delete this object.

        .. versionadded:: 0.4
        """
        assert 'id' in self, 'Missing id attribute.'
        url = '/'.join([self.BASE_URL, str(self['id'])])
        handle_request('delete', url)


class ListableResource(object):
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
                              container=cls.CONTAINER)


class ReloadableResource(object):
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
