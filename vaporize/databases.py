# -*- coding: utf-8 -*-

import json

from vaporize.core import convert_datetime, get_url, handle_request, query
from vaporize.utils import DotDict


class Database(DotDict):
    """A CloudDatabase Database."""
    pass


class Flavor(DotDict):
    """A CloudDatabase Flavor"""
    pass


class Instance(DotDict):
    """A CloudDatabase Instance."""
    def __repr__(self):
        if 'name' in self:
            return '<Instance %s>' % self['name']
        return super(Instance, self).__repr__()

    def __setitem__(self, key, value):
        if key in ['created', 'updated']:
            value = convert_datetime(value)
        elif key == 'flavor':
            value = Flavor(value)
        elif key == 'volume':
            value = Volume(value)
        super(Instance, self).__setitem__(key, value)


class Volume(DotDict):
    """A CloudDatabase Volume."""
    def __repr__(self):
        if 'used' in self and 'size' in self:
            return '<Volume %.2f%%>' % ((self['used'] / self['size']) * 100.0)
        return super(Volume, self).__repr__()


def list():
    """Returns a list of CloudDatabase instances.

    :returns: A list of CloudDatabase instances.
    :rtype: :class:`Instance`

    .. versionadded:: 0.2
    """
    url = '/'.join([get_url('clouddatabases'), 'instances'])
    return handle_request('get', url, wrapper=Instance, container='instances')


def get(id):
    """Returns an Instance by ID.

    :param id: The ID of the Instance to retrieve.
    :type id: int
    :returns: A CloudDatabases Instance matching the ID.
    :rtype: :class:`Instance`

    .. versionadded:: 0.2
    """
    url = '/'.join([get_url('clouddatabases'), 'instances', str(id)])
    return handle_request('get', url, wrapper=Instance, container='instance')


def create(name, server):
    """Create a CloudDatabases Instance.

    :param name: Name of the Image
    :type name: str
    :param server: Server or ``id`` to base the Image upon
    :type server: int or :class:`vaporize.servers.Server`
    :returns: A shiny new CloudServers Image.
    :rtype: :class:`Image`

    .. versionadded:: 0.2
    """
    if isinstance(server, vaporize.servers.Server):
        server = server.id
    server = int(server)
    data = {'image': {'serverId': server,
                      'name': name}}
    data = json.dumps(data)
    url = '/'.join([get_url('cloudservers'), 'images'])
    return handle_request('post', url, data, Image, 'image')
