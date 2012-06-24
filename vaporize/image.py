import json

from vaporize.core import (get_session, get_url, handle_response, munge_url,
                           query)
from vaporize.util import DotDict


class Image(DotDict):
    """A CloudServers Image"""
    def __repr__(self):
        if 'name' in self:
            return '<Image %s>' % self['name']
        return super(Image, self).__repr__()

    def delete(self):
        """Delete this Image

        .. note::

            You can only delete Images you create.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudservers'), 'images', str(self['id'])])
        session = get_session()
        response = session.delete(url)


def list(limit=None, offset=None, detail=False):
    """Returns a list of Images

    :param limit: Limit the result set by a cetain number
    :type limit: int
    :param offset: Offset the result set by a certain number
    :type offset: int
    :param detail: Return additional details about each Image
    :type detail: bool
    :returns: A list of :class:`Image`

    .. versionadded:: 0.1
    """
    url = [get_url('cloudservers'), 'images']
    if detail:
        url.append('detail')
    url = '/'.join(url)
    if limit is not None or offset is not None:
        url = query(url, limit=limit, offset=offset)
    session = get_session()
    response = session.get(munge_url(url))
    return handle_response(response, Image, 'images')


def get(id):
    """Return an Image by ID

    :param id: The ID of the Image to retrieve
    :type id: int
    :returns: :class:`Image`

    .. versionadded:: 0.1
    """
    url = '/'.join([get_url('cloudservers'), 'images', str(id)])
    session = get_session()
    response = session.get(munge_url(url))
    return handle_response(response, Image, 'image')


def create(name, server):
    """Create an Image

    :param name: Name of the Image
    :type name: str
    :param server: :class:`vaporize.server.Server` ``id`` to create Image from
    :type server: int
    :returns: An :class:`Image`

    .. versionadded:: 0.1
    """
    data = {'image': {'serverId': int(server),
                      'name': name}}
    data = json.dumps(data)
    url = '/'.join([get_url('cloudservers'), 'images'])
    session = get_session()
    response = session.post(url, data=data)
    return handle_response(response, Image, 'image')
