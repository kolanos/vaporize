from vaporize.core import get_session, get_url, handle_response, query
from vaporize.util import DotDict


class Flavor(DotDict):
    def __repr__(self):
        return '<Flavor %s>' % self.name


def list(limit=None, offset=None, detail=False):
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
    url = '/'.join([get_url('cloudservers'), 'flavors', str(id)])
    session = get_session()
    response = session.get(url)
    return handle_response(response, Flavor, 'flavor')
