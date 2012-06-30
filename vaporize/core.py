# -*- coding: utf-8 -*-

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

from vaporize.exceptions import ConnectionError, handle_exception

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

    Raises::
        ConnectionError: An error occured while creating the connection/session.
    """
    global _settings, _session
    if region in ['DFW', 'ORD']:
        auth_url = US_AUTH_URL
    elif region == 'LON':
        auth_url = UK_AUTH_URL
    else:
        raise ConnectionError("Unrecognized region %s" % region)
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json'}
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
        _settings['expires'] = dateutil.parser.parse(data['token']['expires'])
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
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'}
        _session = requests.session(auth=auth, headers=headers)
    else:
        raise ConnectionError("HTTP %d: %s" % (response.status_code,
                                               response.content))


def handle_request(verb, url, data=None, wrapper=None, container=None, **kwargs):
    """Handle a request/response in a consistent way."""
    session = get_session()
    if verb == 'get':
        request = session.get
        url = munge_url(url)
    elif verb == 'post':
        request = session.post
    elif verb == 'put':
        request = session.put
    elif verb == 'delete':
        request = session.delete
    response = request(url, data=data)
    if response.status_code not in [200, 201, 202, 203, 204]:
        handle_exception(response.status_code, response.content)
    content = response.content.strip()
    if not content:
        return True
    content = json.loads(content)
    if container and isinstance(content[container], list):
        return [wrapper(i, **kwargs) for i in content[container]]
    elif container is None:
        return wrapper(content, **kwargs)
    else:
        return wrapper(content[container], **kwargs)


def get_session():
    """Return the requests session."""
    return _session


def get_url(service):
    """Return the URL for the specific Rackspace Cloud service."""
    service = '%s_url' % service
    if service in _settings:
        return _settings[service]
    else:
        raise ConnectionError('Not connected to Rackspace Cloud')


def query(url, **kwargs):
    """Append to the URL's query string."""
    scheme, netloc, path, query, fragment = urlsplit(url)
    query = parse_qsl(query)
    for k, v in list(kwargs.items()):
        if v is not None:
            query.append((k, v))
    query = urlencode(query)
    return urlunsplit((scheme, netloc, path, query, fragment))


def munge_url(url):
    """Prevent GET responses from being aggressively cached."""
    scheme, netloc, path, query, fragment = urlsplit(url)
    query = parse_qsl(query)
    query.append(('fresh', str(time.time())))
    query = urlencode(query)
    return urlunsplit((scheme, netloc, path, query, fragment))


def convert_datetime(value):
    return dateutil.parser.parse(value)
