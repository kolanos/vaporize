# -*- coding: utf-8 -*-

import datetime
import json

from vaporize.core import convert_datetime, get_url, handle_request, query
from vaporize.utils import DotDict


class Database(DotDict):
    """A CloudDatabase Database."""
    pass


class Instance(DotDict):
    """A CloudDatabase Instance."""
    pass


def list():
    """Returns a list of database instances.

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
