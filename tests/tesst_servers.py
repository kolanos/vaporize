from functools import partial

from nose.tools import *
from .mock import mock, handle_request_mock

import vaporize


def test_list():
    expected  = '{"flavors":[{"id":1,"name":"256 server"},{"id":2,"name":"512 server"},{"id":3,"name":"1GB server"},{"id":4,"name":"2GB server"},{"id":5,"name":"4GB server"},{"id":6,"name":"8GB server"},{"id":7,"name":"15.5GB server"},{"id":8,"name":"30GB server"}]}'
    handle_mock = partial(handle_request_mock, expected)
    with mock(vaporize.flavors, handle_request=handle_mock):
        flavors = vaporize.flavors.list()
    assert isinstance(flavors, list)
    assert len(flavors) > 0
    for flavor in flavors:
        assert isinstance(flavor, vaporize.flavors.Flavor)
        assert hasattr(flavor, 'id')
        assert hasattr(flavor, 'name')


def test_list_detail():
    expected  = '{"flavors":[{"id":1,"ram":256,"disk":10,"name":"256 server"},{"id":2,"ram":512,"disk":20,"name":"512 server"},{"id":3,"ram":1024,"disk":40,"name":"1GB server"},{"id":4,"ram":2048,"disk":80,"name":"2GB server"},{"id":5,"ram":4096,"disk":160,"name":"4GB server"},{"id":6,"ram":8192,"disk":320,"name":"8GB server"},{"id":7,"ram":15872,"disk":620,"name":"15.5GB server"},{"id":8,"ram":30720,"disk":1200,"name":"30GB server"}]}'
    handle_mock = partial(handle_request_mock, expected)
    with mock(vaporize.flavors, handle_request=handle_mock):
        flavors = vaporize.flavors.list(detail=True)
    assert isinstance(flavors, list)
    assert len(flavors) > 0
    for flavor in flavors:
        assert isinstance(flavor, vaporize.flavors.Flavor)
        assert hasattr(flavor, 'id')
        assert hasattr(flavor, 'name')
        assert hasattr(flavor, 'disk')
        assert hasattr(flavor, 'ram')


def test_list_limit():
    expected  = '{"flavors":[{"id":1,"name":"256 server"},{"id":2,"name":"512 server"},{"id":3,"name":"1GB server"},{"id":4,"name":"2GB server"},{"id":5,"name":"4GB server"}]}'
    handle_mock = partial(handle_request_mock, expected)
    with mock(vaporize.flavors, handle_request=handle_mock):
        flavors = vaporize.flavors.list(limit=5)
    assert isinstance(flavors, list)
    assert len(flavors) == 5


def test_list_offset():
    expected  = '{"flavors":[{"id":6,"name":"8GB server"},{"id":7,"name":"15.5GB server"},{"id":8,"name":"30GB server"}]}'
    handle_mock = partial(handle_request_mock, expected)
    with mock(vaporize.flavors, handle_request=handle_mock):
        flavors = vaporize.flavors.list(offset=5)
    assert isinstance(flavors, list)
    assert flavors[0].id == 6


def test_get():
    expected  = '{"flavor":{"id":1,"ram":256,"disk":10,"name":"256 server"}}'
    handle_mock = partial(handle_request_mock, expected)
    with mock(vaporize.flavors, handle_request=handle_mock):
        flavor = vaporize.flavors.get(1)
    assert isinstance(flavor, vaporize.flavors.Flavor)
    assert hasattr(flavor, 'id')
    assert flavor.id == 1
    assert hasattr(flavor, 'name')
    assert flavor.name == '256 server'
    assert hasattr(flavor, 'disk')
    assert flavor.disk == 10
    assert hasattr(flavor, 'ram')
    assert flavor.ram == 256
