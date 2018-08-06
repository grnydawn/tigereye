# -*- coding: utf-8 -*-
"""topcli name module."""

import string

from .error import UsageError

_builtins = {
    "False":    False,
    "len":      len,
    "max":      max,
    "min":      min,
    "range":    range,
    "True":     True,
}

class Globals(dict):

    def __init__(self, *vargs, **kwargs):
        super(Globals, self).__init__(*vargs, **kwargs)
        self['__builtins__'] = _builtins
        for C in string.ascii_uppercase[:26]:
            self[C] = None

    def __setitem__(self, key, item):
        if key in globals()['__builtins__']:
            raise UsageError("builtin name, '%s', can not be overriden."%key)
        super(Globals, self).__setitem__(key, item)
