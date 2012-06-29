# -*- coding: utf-8 -*-

from vaporize.core import get_url, handle_request, query
from vaporize.utils import DotDict


class Flavor(DotDict):
    """A CloudServers Flavor."""
    def __repr__(self):
        if 'name' in self:
            return '<Flavor %s>' % self['name']
        return super(Flavor, self).__repr__()


def list(limit=None, offset=None, detail=False):
    """Returns a list of Flavors.

    :param limit: Limit the result set by a number
    :type limit: int
    :param offset: Offset the result set by a number
    :type offset: int
    :param detail: Return additional details about each Flavor
    :type: bool
    :returns: A list of CloudServers Flavors.
    :rtype: :class:`Flavor`

    .. versionadded:: 0.1
    """
    url = [get_url('cloudservers'), 'flavors']
    if detail:
        url.append('detail')
    url = '/'.join(url)
    if limit is not None or offset is not None:
        url = query(url, limit=limit, offset=offset)
    return handle_request('get', url, wrapper=Flavor, container='flavors')


def get(id):
    """Returns a Flavor by ID.

    :param id: The ID of the Flavor to retrieve
    :type id: int
    :returns: A CloudServers Flavor matching the ID.
    :rtype: :class:`Flavor`

    .. versionadded:: 0.1
    """
    url = '/'.join([get_url('cloudservers'), 'flavors', str(id)])
    return handle_request('get', url, wrapper=Flavor, container='flavor')
