import json
import vaporize


def get_url_mock(service):
    return 'http://localhost/'


def handle_request_mock(status_code, content, verb, url, data=None, wrapper=None, container=None, **kwargs):
    response = vaporize.utils.DotDict(status_code=status_code, content=content)
    if response.status_code not in [200, 201, 202, 203, 204]:
        vaporize.exceptions.handle_exception(response.status_code, response.content)
    if not response.content:
        return True
    content = json.loads(response.content)
    if container and isinstance(content[container], list):
        return [wrapper(i, **kwargs) for i in content[container]]
    elif container is None:
        return wrapper(content, **kwargs)
    else:
        return wrapper(content[container], **kwargs)



