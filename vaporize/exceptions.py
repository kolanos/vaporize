# -*- coding: utf-8 -*-

import json


class ConnectionError(Exception):
    pass


class BadRequest(Exception):
    pass


class Unauthorized(Exception):
    pass


class Forbidden(Exception):
    pass


class NotFound(Exception):
    pass


class InternalServerError(Exception):
    pass

class ServiceUnavailable(Exception):
    pass


class OverLimit(Exception):
    pass


class BuildInProgress(Exception):
    pass


class BadMediaType(Exception):
    pass


class UnknownError(Exception):
    pass


def handle_exception(code, msg):
    if code == 400:
        raise BadRequest(msg)
    elif code == 401:
        raise Unauthorized(msg)
    elif code == 403:
        raise Forbidden(msg)
    elif code == 404:
        raise NotFound(msg)
    elif code == 409:
        raise BuildInProgress(msg)
    elif code == 413:
        raise OverLimit(msg)
    elif code == 415:
        raise BadMediaType(msg)
    elif code == 500:
        raise InternalServerError(msg)
    elif code == 503:
        raise ServiceUnavailable(msg)
    else:
        raise UnknownError(msg)
