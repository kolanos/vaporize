import json

from vaporize.core import (get_session, get_url, handle_response, munge_url,
                           query)
from vaporize.util import DotDict


class SharedIPGroup(DotDict):
    def __repr__(self):
        return '<SharedIPGroup %s>' % self.name

    def delete(self):
        url = '/'.join([get_url('cloudservers'), 'shared_ip_groups', str(self.id)])
        session = get_session()
        response = session.delete(url)
        return handle_response(response)


def list(limit=None, offset=None, detail=False):
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
    url = '/'.join([get_url('cloudservers'), 'shared_ip_groups', str(id)])
    session = get_session()
    response = session.get(munge_url(url))
    return handle_response(response, SharedIPGroup, 'sharedIpGroup')


def create(name, server):
    data = {'sharedIpGroup': {'name': name,
                              'server': int(server)}}
    data = json.dumps(data)
    url = '/'.join([get_url('cloudservers'), 'server_ip_groups'])
    session = get_session()
    response = session.post(url, data=data)
    return handle_response(response, SharedIPGroup, 'sharedIpGroup')
