from functools import partial

from nose.tools import *
from .mock import mock, handle_request_mock

import vaporize


def test_list():
    expected  = '{"images":[{"id":31,"name":"Windows Server 2008 SP2 (32-bit)"},{"id":85,"name":"Windows Server 2008 R2 (64-bit)"},{"id":100,"name":"Arch 2011.10"},{"id":89,"name":"Windows Server 2008 R2 + SQL Server 2008 R2 Web"},{"id":126,"name":"Fedora 17"},{"id":108,"name":"Gentoo 11.0"},{"id":109,"name":"openSUSE 12"},{"id":110,"name":"Red Hat Enterprise Linux 5.5"},{"id":56,"name":"Windows Server 2008 SP2 (32-bit) + SQL Server 2008 R2 Standard"},{"id":120,"name":"Fedora 16"},{"id":119,"name":"Ubuntu 11.10"},{"id":122,"name":"CentOS 6.2"},{"id":104,"name":"Debian 6 (Squeeze)"},{"id":91,"name":"Windows Server 2008 R2 + SQL Server 2012 Standard"},{"id":115,"name":"Ubuntu 11.04"},{"id":118,"name":"CentOS 6.0"},{"id":86,"name":"Windows Server 2008 R2 + SQL Server 2008 R2 Standard"},{"id":92,"name":"Windows Server 2008 R2 + SQL Server 2012 Web"},{"id":112,"name":"Ubuntu 10.04 LTS"},{"id":24,"name":"Windows Server 2008 SP2 (64-bit)"},{"id":121,"name":"CentOS 5.8"},{"id":111,"name":"Red Hat Enterprise Linux 6"},{"id":116,"name":"Fedora 15"},{"id":125,"name":"Ubuntu 12.04 LTS"},{"id":114,"name":"CentOS 5.6"},{"id":103,"name":"Debian 5 (Lenny)"},{"id":57,"name":"Windows Server 2008 SP2 (64-bit) + SQL Server 2008 R2 Standard"}]}'
    handle_mock = partial(handle_request_mock, expected)
    with mock(vaporize.images, handle_request=handle_mock):
        images = vaporize.images.list()
    assert isinstance(images, list)
    assert len(images) > 0
    for image in images:
        assert isinstance(image, vaporize.images.Image)
        assert hasattr(image, 'id')
        assert hasattr(image, 'name')


def test_list_detail():
    expected  = '{"images":[{"id":31,"status":"ACTIVE","updated":"2010-01-26T12:07:44-06:00","name":"Windows Server 2008 SP2 (32-bit)"},{"id":85,"status":"ACTIVE","updated":"2010-01-26T12:07:17-06:00","name":"Windows Server 2008 R2 (64-bit)"},{"id":100,"status":"ACTIVE","updated":"2011-09-12T09:09:23-05:00","name":"Arch 2011.10"},{"id":89,"status":"ACTIVE","updated":"2011-10-04T08:39:34-05:00","name":"Windows Server 2008 R2 + SQL Server 2008 R2 Web"},{"id":126,"status":"ACTIVE","updated":"2012-05-29T17:11:45-05:00","name":"Fedora 17"},{"id":108,"status":"ACTIVE","updated":"2011-11-01T08:32:30-05:00","name":"Gentoo 11.0"},{"id":109,"status":"ACTIVE","updated":"2011-11-03T06:28:56-05:00","name":"openSUSE 12"},{"id":110,"status":"ACTIVE","updated":"2011-08-17T05:11:30-05:00","name":"Red Hat Enterprise Linux 5.5"},{"id":56,"status":"ACTIVE","updated":"2010-09-17T07:12:56-05:00","name":"Windows Server 2008 SP2 (32-bit) + SQL Server 2008 R2 Standard"},{"id":120,"status":"ACTIVE","updated":"2012-01-03T04:39:05-06:00","name":"Fedora 16"},{"id":119,"status":"ACTIVE","updated":"2011-11-03T08:55:15-05:00","name":"Ubuntu 11.10"},{"id":122,"status":"ACTIVE","updated":"2012-02-06T04:34:21-06:00","name":"CentOS 6.2"},{"id":104,"status":"ACTIVE","updated":"2011-08-17T05:11:30-05:00","name":"Debian 6 (Squeeze)"},{"id":91,"status":"ACTIVE","updated":"2012-04-24T16:44:01-05:00","name":"Windows Server 2008 R2 + SQL Server 2012 Standard"},{"id":115,"status":"ACTIVE","updated":"2011-08-17T05:11:30-05:00","name":"Ubuntu 11.04"},{"id":118,"status":"ACTIVE","updated":"2011-08-17T05:11:30-05:00","name":"CentOS 6.0"},{"id":86,"status":"ACTIVE","updated":"2010-09-17T07:19:20-05:00","name":"Windows Server 2008 R2 + SQL Server 2008 R2 Standard"},{"id":92,"status":"ACTIVE","updated":"2012-04-24T16:44:01-05:00","name":"Windows Server 2008 R2 + SQL Server 2012 Web"},{"id":112,"status":"ACTIVE","updated":"2011-04-21T10:24:01-05:00","name":"Ubuntu 10.04 LTS"},{"id":24,"status":"ACTIVE","updated":"2010-01-26T12:07:04-06:00","name":"Windows Server 2008 SP2 (64-bit)"},{"id":121,"status":"ACTIVE","updated":"2012-05-04T10:51:28-05:00","name":"CentOS 5.8"},{"id":111,"status":"ACTIVE","updated":"2011-09-12T10:53:12-05:00","name":"Red Hat Enterprise Linux 6"},{"id":116,"status":"ACTIVE","updated":"2011-08-17T05:11:30-05:00","name":"Fedora 15"},{"id":125,"status":"ACTIVE","updated":"2012-05-03T07:21:06-05:00","name":"Ubuntu 12.04 LTS"},{"id":114,"status":"ACTIVE","updated":"2011-08-17T05:11:30-05:00","name":"CentOS 5.6"},{"id":103,"status":"ACTIVE","updated":"2011-08-17T05:11:30-05:00","name":"Debian 5 (Lenny)"},{"id":57,"status":"ACTIVE","updated":"2010-09-17T07:16:25-05:00","name":"Windows Server 2008 SP2 (64-bit) + SQL Server 2008 R2 Standard"}]}'
    handle_mock = partial(handle_request_mock, expected)
    with mock(vaporize.images, handle_request=handle_mock):
        images = vaporize.images.list(detail=True)
    assert isinstance(images, list)
    assert len(images) > 0
    for image in images:
        assert isinstance(image, vaporize.images.Image)
        assert hasattr(image, 'id')
        assert hasattr(image, 'name')
        assert hasattr(image,'status')
        assert hasattr(image, 'updated')


def test_list_limit():
    expected  = '{"images":[{"id":31,"name":"Windows Server 2008 SP2 (32-bit)"},{"id":85,"name":"Windows Server 2008 R2 (64-bit)"},{"id":100,"name":"Arch 2011.10"},{"id":89,"name":"Windows Server 2008 R2 + SQL Server 2008 R2 Web"},{"id":126,"name":"Fedora 17"}]}'
    handle_mock = partial(handle_request_mock, expected)
    with mock(vaporize.images, handle_request=handle_mock):
        images = vaporize.images.list(limit=5)
    assert isinstance(images, list)
    assert len(images) == 5


def test_list_offset():
    expected  = '{"images":[{"id":108,"name":"Gentoo 11.0"},{"id":109,"name":"openSUSE 12"},{"id":110,"name":"Red Hat Enterprise Linux 5.5"},{"id":56,"name":"Windows Server 2008 SP2 (32-bit) + SQL Server 2008 R2 Standard"},{"id":120,"name":"Fedora 16"},{"id":119,"name":"Ubuntu 11.10"},{"id":122,"name":"CentOS 6.2"},{"id":104,"name":"Debian 6 (Squeeze)"},{"id":91,"name":"Windows Server 2008 R2 + SQL Server 2012 Standard"},{"id":115,"name":"Ubuntu 11.04"},{"id":118,"name":"CentOS 6.0"},{"id":86,"name":"Windows Server 2008 R2 + SQL Server 2008 R2 Standard"},{"id":92,"name":"Windows Server 2008 R2 + SQL Server 2012 Web"},{"id":112,"name":"Ubuntu 10.04 LTS"},{"id":24,"name":"Windows Server 2008 SP2 (64-bit)"},{"id":121,"name":"CentOS 5.8"},{"id":111,"name":"Red Hat Enterprise Linux 6"},{"id":116,"name":"Fedora 15"},{"id":125,"name":"Ubuntu 12.04 LTS"},{"id":114,"name":"CentOS 5.6"},{"id":103,"name":"Debian 5 (Lenny)"},{"id":57,"name":"Windows Server 2008 SP2 (64-bit) + SQL Server 2008 R2 Standard"}]}'
    handle_mock = partial(handle_request_mock, expected)
    with mock(vaporize.images, handle_request=handle_mock):
        images = vaporize.images.list(offset=5)
    assert isinstance(images, list)
    assert images[0].id == 108


def test_get():
    expected  = '{"image":{"id":112,"status":"ACTIVE","created":"2011-04-21T10:24:01-05:00","updated":"2011-04-21T10:24:01-05:00","name":"Ubuntu 10.04 LTS"}}'
    handle_mock = partial(handle_request_mock, expected)
    with mock(vaporize.images, handle_request=handle_mock):
        image = vaporize.images.get(112)
    assert isinstance(image, vaporize.images.Image)
    assert hasattr(image, 'id')
    assert image.id == 112
    assert hasattr(image, 'name')
    assert image.name == 'Ubuntu 10.04 LTS'
    assert hasattr(image, 'status')
    assert image.status == 'ACTIVE'


def test_create():
    expected = '{"image":{"id":12345,"status":"QUEUED","updated":"2012-07-13T17:26:24-05:00","name":"testing","serverId":54321}}'
    handle_mock = partial(handle_request_mock, expected)
    with mock(vaporize.images, handle_request=handle_mock):
        image = vaporize.images.create('testing', 54321)
    assert isinstance(image, vaporize.images.Image)
    assert hasattr(image, 'id')
    assert image.id == 12345
    assert hasattr(image, 'name')
    assert image.name == 'testing'
    assert hasattr(image, 'server_id')
    assert image.server_id == 54321
    assert hasattr(image, 'status')
    assert image.status == 'QUEUED'


def test_reload():
    expected = '{"image":{"progress":100,"id":12345,"status":"ACTIVE","created":"2012-07-13T17:26:23-05:00","updated":"2012-07-13T17:29:10-05:00","name":"testing"}}'
    handle_mock = partial(handle_request_mock, expected)
    with mock(vaporize.images, handle_request=handle_mock):
        image = vaporize.images.get(12345)
        image.reload()
    assert isinstance(image, vaporize.images.Image)
    assert hasattr(image, 'id')
    assert image.id == 12345
