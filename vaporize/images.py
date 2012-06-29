# -*- coding: utf-8 -*-

import json

from vaporize.core import convert_datetime, get_url, handle_request, query
import vaporize.servers
from vaporize.utils import DotDict


class Image(DotDict):
    """A CloudServers Image."""
    def __repr__(self):
        if 'name' in self:
            return '<Image %s>' % self['name']
        return super(Image, self).__repr__()

    def __setitem__(self, key, value):
        if key == 'serverId':
            key = 'server_id'
        elif key in ['created', 'updated']:
            value = convert_datetime(value)
        super(Image, self).__setitem__(key, value)

    def delete(self):
        """Delete this Image.

        .. note::

            You can only delete Images you create.

        .. warning::

            There is not confirmation step for this operation. Deleting an
            image is permanent.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudservers'), 'images', str(self['id'])])
        handle_request('delete', url)


def list(limit=None, offset=None, detail=False):
    """Returns a list of CloudServers Images.

    :param limit: Limit the result set by a cetain number
    :type limit: int
    :param offset: Offset the result set by a certain number
    :type offset: int
    :param detail: Return additional details about each Image
    :type detail: bool
    :returns: A list of CloudServers Images.
    :rtype: A list of :class:`Image`

    .. versionadded:: 0.1
    """
    url = [get_url('cloudservers'), 'images']
    if detail:
        url.append('detail')
    url = '/'.join(url)
    if limit is not None or offset is not None:
        url = query(url, limit=limit, offset=offset)
    return handle_request('get', url, wrapper=Image, container='images')


def get(id):
    """Return an Image by ID.

    :param id: The ID of the Image to retrieve
    :type id: int
    :returns: A CloudServer Image matching the ID.
    :rtype: :class:`Image`

    .. versionadded:: 0.1
    """
    url = '/'.join([get_url('cloudservers'), 'images', str(id)])
    return handle_request('get', url, wrapper=Image, container='image')


def create(name, server):
    """Create an Image.

    :param name: Name of the Image
    :type name: str
    :param server: Server or ``id`` to base the Image upon
    :type server: int or :class:`vaporize.servers.Server`
    :returns: A shiny new CloudServers Image.
    :rtype: :class:`Image`

    .. versionadded:: 0.1
    """
    if isinstance(server, vaporize.servers.Server):
        server = server.id
    server = int(server)
    data = {'image': {'serverId': server,
                      'name': name}}
    data = json.dumps(data)
    url = '/'.join([get_url('cloudservers'), 'images'])
    return handle_request('post', url, data, Image, 'image')
