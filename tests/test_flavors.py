from functools import partial

from nose.tools import *
from .mock import mock, handle_request_mock

import vaporize


def test_list():
    expected = '{"servers":[{"id":12345,"name":"foo"},{"id":12346,"name":"bar"},{"id":12347,"name":"baz"}]}'
    handle_mock = partial(handle_request_mock, expected)
    with mock(vaporize.servers, handle_request=handle_mock):
        servers = vaporize.servers.list()
    assert isinstance(servers, list)
    assert len(servers) > 0
    for server in servers:
        assert isinstance(server, vaporize.servers.Server)
        assert hasattr(server, 'id')
        assert hasattr(server, 'name')


def test_list_detail():
    expected = '{"servers":[{"progress":0,"id":12345,"imageId":112,"flavorId":4,"status":"ACTIVE","name":"foo","hostId":"asdfasdfasdfasdfasdf","addresses":{"public":["198.0.0.1"],"private":["10.0.0.1"]},"metadata":{}},{"progress":0,"id":12346,"imageId":112,"flavorId":4,"status":"ACTIVE","name":"bar","hostId":"asdfasdfasdfasdfasdf","addresses":{"public":["198.0.0.2"],"private":["10.0.0.2"]},"metadata":{}},{"progress":0,"id":12347,"imageId":112,"flavorId":5,"status":"ACTIVE","name":"baz","hostId":"asdfasdfasdfasdfasdf","addresses":{"public":["198.0.0.3"],"private":["10.0.0.3"]},"metadata":{}}]}'
    handle_mock = partial(handle_request_mock, expected)
    with mock(vaporize.servers, handle_request=handle_mock):
        servers = vaporize.servers.list(detail=True)
    assert isinstance(servers, list)
    assert len(servers) > 0
    for server in servers:
        assert isinstance(server, vaporize.servers.Server)
        assert hasattr(server, 'id')
        assert hasattr(server, 'name')
        assert hasattr(server, 'image_id')
        assert hasattr(server, 'flavor_id')
        assert hasattr(server, 'addresses')
        assert hasattr(server, 'host_id')
        assert hasattr(server, 'status')


def test_list_limit():
    expected = '{"servers":[{"id":12345,"name":"foo"},{"id":12346,"name":"bar"}]}'
    handle_mock = partial(handle_request_mock, expected)
    with mock(vaporize.servers, handle_request=handle_mock):
        servers = vaporize.servers.list(limit=2)
    assert isinstance(servers, list)
    assert len(servers) == 2


def test_list_offset():
    expected = '{"servers":[{"id":12346,"name":"bar"},{"id":12347,"name":"baz"}]}'
    handle_mock = partial(handle_request_mock, expected)
    with mock(vaporize.servers, handle_request=handle_mock):
        servers = vaporize.servers.list(offset=1)
    assert isinstance(servers, list)
    assert servers[0].id == 12346


def test_get():
    expected = '{"server":{"progress":0,"id":12345,"imageId":112,"flavorId":4,"status":"ACTIVE","name":"foo","hostId":"asdfasdfasdfasdfasdf","addresses":{"public":["198.0.0.1"],"private":["10.0.0.1"]},"metadata":{}}}'
    handle_mock = partial(handle_request_mock, expected)
    with mock(vaporize.servers, handle_request=handle_mock):
        server = vaporize.servers.get(12345)
    assert isinstance(server, vaporize.servers.Server)
    assert hasattr(server, 'id')
    assert server.id == 12345
    assert hasattr(server, 'name')
    assert server.name == 'foo'
