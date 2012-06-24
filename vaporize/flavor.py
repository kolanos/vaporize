from vaporize.core import get_session, get_url, handle_response, query
from vaporize.util import DotDict


class Flavor(DotDict):
    """A CloudServers Flavor"""
    def __repr__(self):
        if 'name' in self:
            return '<Flavor %s>' % self['name']
        return super(Flavor, self).__repr__()


def list(limit=None, offset=None, detail=False):
    """Returns a list of Flavors
    
    :param limit: Limit the result set by a number
    :type limit: int
    :param offset: Offset the result set by a number
    :type offset: int
    :param detail: Return additional details about each Flavor
    :type: bool
    :returns: A :class:`Flavor`

    .. versionadded:: 0.1
    """
    url = [get_url('cloudservers'), 'flavors']
    if detail:
        url.append('detail')
    url = '/'.join(url)
    if limit is not None or offset is not None:
        url = query(url, limit=limit, offset=offset)
    session = get_session()
    response = session.get(url)
    return handle_response(response, Flavor, 'flavors')


def get(id):
    """Returns a Flavor by ID
    
    :param id: The ID of the Flavor to retrieve
    :type id: int
    :returns: A :class:`Flavor`

    .. versionadded:: 0.1
    """
    url = '/'.join([get_url('cloudservers'), 'flavors', str(id)])
    session = get_session()
    response = session.get(url)
    return handle_response(response, Flavor, 'flavor')
