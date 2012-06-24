import json

from vaporize.core import (get_session, get_url, handle_response, munge_url,
                           query)
from vaporize.util import DotDict


class SharedIPGroup(DotDict):
    """A Cloudservers Shared IP Group"""
    def __repr__(self):
        if 'name' in self:
            return '<SharedIPGroup %s>' % self['name']
        return super(SharedIPGroup, self).__repr__()

    def __setitem__(self, key, value):
        if key == 'sharedIpGroupId':
            super(SharedIPGroup, self).__setitem__('id', value)
        elif key == 'configuredServer':
            super(SharedIPGroup, self).__setitem__('configured', bool(value))
        else:
            super(SharedIPGroup, self).__setitem__(key, value)

    def delete(self):
        """Delete this Shared IP Group
        
        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudservers'), 'shared_ip_groups', str(self['id'])])
        session = get_session()
        response = session.delete(url)
        handle_response(response)


def list(limit=None, offset=None, detail=False):
    """Returns a list of Shared IP Groups

    :param limit: Limit the result set by a certain number
    :type limit: int
    :param offset: Offset the result set by a certain number
    :type offset: int
    :param detail: Return additional details about each Shared IP Group
    :type detail: bool
    :returns: A list of :class:`SharedIPGroup`

    .. versionadded:: 0.1
    """
    url = [get_url('cloudservers'), 'shared_ip_groups']
    if detail:
        url.append('detail')
    url = '/'.join(url)
    if limit is not None or offset is not None:
        url = query(url, limit=limit, offset=offset)
    session = get_session()
    response = session.get(munge_url(url))
    return handle_response(response, SharedIPGroup, 'sharedIpGroups')


def get(id):
    """Return a Shared IP Group by ID

    :param id: The ID of the Shared IP Group to retrieve
    :type id: int
    :returns: A :class:`SharedIPGroup`

    .. versionadded:: 0.1
    """
    url = '/'.join([get_url('cloudservers'), 'shared_ip_groups', str(id)])
    session = get_session()
    response = session.get(munge_url(url))
    return handle_response(response, SharedIPGroup, 'sharedIpGroup')


def create(name, server):
    """Create a Shared IP Group

    :param name: Name of the Shared IP Group
    :type name: str
    :param server: The :class:`vaporize.server.Server```id`` to add to group
    :type server: int
    :returns: A :class:`SharedIPGroup`

    .. versionadded:: 0.1
    """
    data = {'sharedIpGroup': {'name': name,
                              'server': int(server)}}
    data = json.dumps(data)
    url = '/'.join([get_url('cloudservers'), 'server_ip_groups'])
    session = get_session()
    response = session.post(url, data=data)
    return handle_response(response, SharedIPGroup, 'sharedIpGroup')
