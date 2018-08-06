# -*- coding: utf-8 -*-
"tigereye task module."

import abc
import string
import argparse

from .error import InternalError, UsageError
from .util import subclasses, funcargs_eval, error_warn, args_pop

class Task(object):

    __metaclass__ = abc.ABCMeta

    def __new__(cls, targv):

        parser = argparse.ArgumentParser(description='tigereye %s'%cls.__name__)

        parser.add_argument('--import-task', metavar='task', action='append', help='import task')
        parser.add_argument('--import-function', metavar='function', action='append', help='import function')
        parser.add_argument('--import-module', metavar='module', action='append', help='import module')
        parser.add_argument('--name', metavar='task name', help='task name')
        parser.add_argument('--calc', metavar='calc', action='append', help='python code for manipulating data.')
        parser.add_argument('--output', metavar='output', action='append', help='output variable.')

        targv, add_opts = args_pop(targv, "--add-option", 1)
        targv, discard_opts = args_pop(targv, "--discard-option", 1)

        for opt in add_opts:
            import pdb; pdb.set_trace()

        _discard_opts = []
        for opt in discard_opts:
            opt = opt.strip()
            if opt.startswith("--"):
                opt = opt[2:]
            elif opt.startswith("-"):
                opt = opt[1:]
            opt.replace("-", "_")

            _discard_opts.append(opt)

        obj = super(Task, cls).__new__(cls)
        obj.parser = parser
        obj.targs = None
        obj._discard_options = _discard_opts

        return obj

    @abc.abstractmethod
    def __init__(self, targv):
        pass

    def run(self, gvars):

        assert self.targs is not None

        if self.targs.import_task:
            self.targs.import_task = None

        if self.targs.import_function:
            self.targs.import_function = None

        if self.targs.import_module:
            self.targs.import_module = None

        for opt in self._discard_options:
            setattr(self.targs, opt, None)

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
                error_warn("'%s' is a reserved word."%k)

