import json
import time
import urllib
import urlparse

import requests

from vaporize.exceptions import ConnectionError, handle_exception

US_AUTH_URL = "https://identity.api.rackspacecloud.com/v1.1/auth"
UK_AUTH_URL = "https://lon.identity.api.rackspacecloud.com/v1.1/auth"

_settings = {}
_session = {}


class Auth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['X-Auth-Token'] = self.token
        return r


def connect(user, apikey, region='DFW'):
    global _settings, _session
    if region in ['DFW', 'ORD']:
        auth_url = US_AUTH_URL
    elif region == 'LON':
        auth_url = UK_AUTH_URL
    else:
        raise ConnectionError("Unrecognized region %s" % region)
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json'}
    data = json.dumps({'credentials': {'username': user,
                                       'key': apikey}})
    response = requests.post(auth_url, headers=headers, data=data)
    if response.status_code in [200, 203]:
        data = json.loads(response.content)['auth']
        _settings['token'] = data['token']['id']
        _settings['expires'] = data['token']['expires']
        for s, r in data['serviceCatalog'].items():
            if len(r) == 1:
                _settings[s.lower() + '_url'] = r[0]['publicURL']
            elif len(r) > 1:
                for i in r:
                    if i['region'] == region:
                        _settings[s.lower() + '_url'] = i['publicURL']
        auth = Auth(_settings['token'])
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'}
        _session = requests.session(auth=auth, headers=headers)
    else:
        raise ConnectionError("HTTP %d: %s" % (response.status_code,
                                               response.content))


def handle_response(response, wrapper=None, container=None, **kwargs):
    if response.status_code in [200, 201, 202, 203, 204]:
        if not response.content.strip():
            return True
        data = json.loads(response.content)
        if isinstance(data[container], list):
            return [wrapper(i, **kwargs) for i in data[container]]
        elif container is None:
            return wrapper(data, **kwargs)
        else:
            return wrapper(data[container], **kwargs)
    else:
        handle_exception(response.status_code, response.content)


def get_session():
    return _session


def get_url(service):
    service = '%s_url' % service
    if service in _settings:
        return _settings[service]
    else:
        raise ConnectionError('Not connected to Rackspace Cloud')


def query(url, **kwargs):
    scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
    query = urlparse.parse_qsl(query)
    for k, v in kwargs.items():
        if v is not None:
            query.append((k, v))
    query = urllib.urlencode(query)
    return urlparse.urlunsplit((scheme, netloc, path, query, fragment))


def munge_url(url):
    scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
    query = urlparse.parse_qsl(query)
    query.append(('fresh', str(time.time())))
    query = urllib.urlencode(query)
    return urlparse.urlunsplit((scheme, netloc, path, query, fragment))
