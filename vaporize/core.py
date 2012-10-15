# -*- coding: utf-8 -*-

import datetime
import json
import time
try:
    # Python 3.x
    from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
except ImportError:
    # Python 2.x
    from urllib import urlencode
    from urlparse import parse_qsl, urlsplit, urlunsplit

import dateutil.parser
import requests

from vaporize import __version__
from vaporize.exceptions import ConnectionError, handle_exception
from vaporize.utils import DotDict

US_AUTH_URL = "https://identity.api.rackspacecloud.com/v2.0/tokens"
UK_AUTH_URL = "https://lon.identity.api.rackspacecloud.com/v2.0/tokens"

_settings = {}
_session = {}


class Auth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['X-Auth-Token'] = self.token
        return r


def connect(user, apikey, region='DFW'):
    """Create a session with the Rackspace Cloud API.

    .. note::

        Region support is not universal across all Rackspace Cloud services.

    :param user: A Rackspace Cloud username.
    :type user: str
    :param apikey: A Rackspace Cloud API key.
    :type apikey: str
    :param region: A Rackspace Cloud region, such as ``DFW``, ``ORD`` or ``LON``.
    :type region: str
    :raises: ConnectionError

    .. versionadded:: 0.1
    """
    global _settings, _session
    if region in ['DFW', 'ORD']:
        auth_url = US_AUTH_URL
    elif region == 'LON':
        auth_url = UK_AUTH_URL
    else:
        raise ConnectionError("Unrecognized region %s" % region)
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'User-Agent': 'vaporize/%s' % __version__}
    data = json.dumps({'auth': {
        'RAX-KSKEY:apiKeyCredentials': {
            'username': user,
            'apiKey': apikey
            }
        }})
    response = requests.post(auth_url, headers=headers, data=data)
    if response.status_code in [200, 203]:
        data = json.loads(response.content)['access']
        _settings['token'] = data['token']['id']
        _settings['expires'] = convert_datetime(data['token']['expires'])
        for service in data['serviceCatalog']:
            name = service['name'].lower()
            if len(service['endpoints']) == 1:
                url = service['endpoints'][0]['publicURL']
            else:
                for endpoint in service['endpoints']:
                    if endpoint['region'] == region:
                        url = endpoint['publicURL']
            _settings[name + '_url'] = url
        auth = Auth(_settings['token'])
        _session = requests.session(auth=auth, headers=headers)
    else:
        raise ConnectionError("HTTP %d: %s" % (response.status_code,
                                               response.content))


def handle_request(verb, url, data=None, wrapper=None, container=None, **kwargs):
    if not isinstance(_session, requests.sessions.Session):
        raise ConnectionError('Not connected to the Rackspace Cloud API.')
    if verb == 'get':
        request = _session.get
        url = munge_url(url)
    elif verb == 'post':
        request = _session.post
    elif verb == 'put':
        request = _session.put
    elif verb == 'delete':
        request = _session.delete
    response = request(url, data=data)
    if response.status_code not in [200, 201, 202, 203, 204]:
        handle_exception(response.status_code, response.content)
    content = response.content.strip()
    if not content:
        return True
    content = json.loads(content)
    if wrapper is None:
        wrapper = DotDict
    if container and isinstance(content[container], list):
        return [wrapper(i, **kwargs) for i in content[container]]
    elif container is None:
        return wrapper(content, **kwargs)
    else:
        return wrapper(content[container], **kwargs)


def get_session():
    return _session


def get_url(service):
    service = '%s_url' % service
    if service in _settings:
        return _settings[service]
    else:
        raise ConnectionError('Not connected to Rackspace Cloud')


def query(url, **kwargs):
    scheme, netloc, path, query, fragment = urlsplit(url)
    query = parse_qsl(query)
    for k, v in list(kwargs.items()):
        if v is not None:
            query.append((k, v))
    query = urlencode(query)
    return urlunsplit((scheme, netloc, path, query, fragment))


def munge_url(url):
    scheme, netloc, path, query, fragment = urlsplit(url)
    query = parse_qsl(query)
    query.append(('fresh', str(time.time())))
    query = urlencode(query)
    return urlunsplit((scheme, netloc, path, query, fragment))


def convert_datetime(value):
    if not isinstance(value, datetime.datetime):
        value = dateutil.parser.parse(value)
    return value
