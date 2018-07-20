# -*- coding: utf-8 -*-
"tigereye task module."

import abc

from .error import InternalError
from .util import subclasses

class Task(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, targv):
        pass

    def run(self, gvars):
        newgvars = dict(gvars)
        self.perform(newgvars)

    @abc.abstractmethod
    def perform(self, gvars):
        pass
