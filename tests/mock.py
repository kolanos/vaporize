import json

from vaporize.exceptions import handle_exception
from vaporize.utils import DotDict


class mock(object):
    """Super simple mocking context manager.

        Example::

            import foo
            from cStringIO import StringIO
            from mock import mock

            def test_get_data():
                expected = 'Mary had a little lamb'
                with mock(foo, urlopen=lambda url: StringIO(expected)):
                    result = foo.get_data('http://google.com')
                assert result == expected, 'bad data'
    """
    def __init__(self, obj, **kw):
        '''Create mock object
            obj - Object to be mocked
            kw - Mocked attributes
        '''
        self.obj = obj
        self.mocks = kw.copy()

    def __enter__(self):
        self.orig = self.obj.__dict__.copy()
        self.obj.__dict__.update(self.mocks)
        return self

    def __exit__(self, type, value, trackback):
        self.obj.__dict__.update(self.orig)


def handle_request_mock(status_code, content, verb, url, data=None, wrapper=None, container=None, **kwargs):
    response = DotDict(status_code=status_code, content=content)
    if response.status_code not in [200, 201, 202, 203, 204]:
        handle_exception(response.status_code, response.content)
    if not response.content:
        return True
    content = json.loads(response.content)
    if container and isinstance(content[container], list):
        return [wrapper(i, **kwargs) for i in content[container]]
    elif container is None:
        return wrapper(content, **kwargs)
    else:
        return wrapper(content[container], **kwargs)
