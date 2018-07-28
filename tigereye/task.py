# -*- coding: utf-8 -*-
"tigereye task module."

import abc
import string
import argparse

from .error import InternalError, UsageError, UsageWarning
from .util import subclasses, funcargs_eval

class Task(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, targv):
        pass

    def run(self, gvars):

        assert hasattr(self, 'targs') and isinstance(self.targs, argparse.Namespace)

        if self.targs.import_task:
            self.targs.import_task = None

        if self.targs.import_function:
            self.targs.import_function = None

        newgvars = dict(gvars)

        if hasattr(self.targs, 'calc') and self.targs.calc:
            for calc in self.targs.calc:
                self.handle_calc_opt(calc, newgvars)

        out = self.perform(newgvars)

        if hasattr(self.targs, 'output') and self.targs.output:
            for output_arg in self.targs.output:
                s = output_arg.split("$")
                vargs, kwargs = funcargs_eval(s[0], s[1:], newgvars)
                for k, v in kwargs.items():
                    if k not in string.ascii_uppercase[:26]:
                        gvars[k] = v
                    else:
                        raise UsageError("'%s' is a reserved word."%k)

    @abc.abstractmethod
    def perform(self, gvars):
        pass

    def handle_calc_opt(self, calc, gvars):
        s = calc.split("$")
        vargs, kwargs = funcargs_eval(s[0], s[1:], gvars)
        for k, v in kwargs.items():
            if k not in string.ascii_uppercase[:26]:
                gvars[k] = v
            else:
                raise UsageWarning("'%s' is a reserved word."%k)

