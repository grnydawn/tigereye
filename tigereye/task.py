# -*- coding: utf-8 -*-
"tigereye task module."

import abc
import string

from .error import InternalError, UsageError
from .util import subclasses

class Task(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, targv):
        pass

    def run(self, gvars):
        newgvars = dict(gvars)
        out = self.perform(newgvars)
        if isinstance(out, dict):
            for k, v in out.items():
                if k not in string.ascii_uppercase[:26]:
                    gvars[k] = v
                else:
                    raise UsageError("'%s' is a reserved word."%k)

    @abc.abstractmethod
    def perform(self, gvars):
        pass
