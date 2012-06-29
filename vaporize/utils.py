# -*- coding: utf-8 -*-

import re


class DotDict(dict):
    """
    Give dict support for dot notation and force value changes through
    __setitem__ so that it can be overloaded/overidden.
    """
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def update(self, *args, **kwargs):
        if len(args) > 1:
            raise TypeError("update expected at most 1 arguments, got %d" % len(args))
        other = dict(*args, **kwargs)
        for key in other:
            self[key] = other[key]

    def setdefault(self, key, value=None):
        if key not in self:
            self[key] = value
        return self[key]

    def __setitem__(self, key,value):
        key = camelcase_to_underscore(key)
        super(DotDict, self).__setitem__(key, value)

    __setattr__ = __setitem__
    __getattr__ = dict.__getitem__
    __delattr__ = dict.__delitem__

camelcase_to_underscore = lambda str: re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '_\\1', str).lower().strip('_')
