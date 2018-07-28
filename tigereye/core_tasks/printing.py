# -*- coding: utf-8 -*-
"tigereye print core task module."

import os
import argparse

from ..task import Task
from ..error import UsageError
from ..util import funcargs_eval, parse_subargs

class print_task(Task):

    def __init__(self, targv):

        parser = argparse.ArgumentParser(description='tigereye printing task')
        parser.add_argument("-s", '--str', metavar='str', action='append', help='run str()')
        parser.add_argument('--shape', metavar='data shape', action='append', help='data shape')
        parser.add_argument('--ndim', metavar='data dimension', action='append', help='data dimension')
        parser.add_argument('--head', metavar='data head', action='append', help='data head')
        parser.add_argument('--tail', metavar='data tail', action='append', help='data tail')
        parser.add_argument('--dtypes', metavar='data types', action='append', help='data types')
        parser.add_argument('--describe', metavar='data description', action='append', help='data description')
        parser.add_argument('--count', metavar='element count', action='append', help='data element count')
        parser.add_argument('--max', metavar='max value', action='append', help='maximum element')
        parser.add_argument('--min', metavar='min value', action='append', help='minimum element')
        parser.add_argument('--mean', metavar='mean value', action='append', help='mean value')
        parser.add_argument('--std', metavar='std value', action='append', help='standard deviation value')
        parser.add_argument('--calc', metavar='calc', action='append', help='python code for manipulating data.')
        parser.add_argument('--import-task', metavar='task', action='append', help='import task')
        parser.add_argument('--import-function', metavar='function', action='append', help='import function')
        parser.add_argument('--output', metavar='output', action='append', help='output variable.')
        parser.add_argument('--name', metavar='task name', help='task name')
        parser.add_argument('--version', action='version', version='tigereye printing task version 0.0.0')

        self.targs = parser.parse_args(targv)

    def perform(self, gvars):

        printed = set()

        def _print(obj):
            print("\n"+str(obj))
            printed.add(True)

        if self.targs.shape:
            for shape_arg in self.targs.shape:
                s = pandas_arg.split("$")
                vargs, kwargs = funcargs_eval(s[0], s[1:], gvars)
                for varg in vargs:
                    _print(getattr(varg, 'shape'))

        if self.targs.ndim:
            for ndim_arg in self.targs.ndim:
                s = pandas_arg.split("$")
                vargs, kwargs = funcargs_eval(s[0], s[1:], gvars)
                for varg in vargs:
                    _print(getattr(varg, 'ndim'))

        if self.targs.dtypes:
            for dtypes_arg in self.targs.dtypes:
                s = pandas_arg.split("$")
                vargs, kwargs = funcargs_eval(s[0], s[1:], gvars)
                for varg in vargs:
                    _print(getattr(varg, 'dtypes'))

        if self.targs.head:
            for head_arg in self.targs.head:
                s = head_arg.split("$")
                lvargs, lkwargs, rvargs, rkwargs = \
                    parse_subargs(s[0], s[1:], gvars)
                for lvarg in lvargs:
                    _print(getattr(lvarg, "head")(*rvargs, **rkwargs))

        if self.targs.tail:
            for tail_arg in self.targs.tail:
                s = tail_arg.split("$")
                lvargs, lkwargs, rvargs, rkwargs = \
                    parse_subargs(s[0], s[1:], gvars)
                for lvarg in lvargs:
                    _print(getattr(lvarg, "tail")(*rvargs, **rkwargs))

        if self.targs.describe:
            for describe_arg in self.targs.describe:
                s = describe_arg.split("$")
                lvargs, lkwargs, rvargs, rkwargs = \
                    parse_subargs(s[0], s[1:], gvars)
                for lvarg in lvargs:
                    _print(getattr(lvarg, "describe")(*rvargs, **rkwargs))

        if self.targs.count:
            for count_arg in self.targs.count:
                s = count_arg.split("$")
                lvargs, lkwargs, rvargs, rkwargs = \
                    parse_subargs(s[0], s[1:], gvars)
                for lvarg in lvargs:
                    _print(getattr(lvarg, "count")(*rvargs, **rkwargs))

        if self.targs.max:
            for max_arg in self.targs.max:
                s = max_arg.split("$")
                lvargs, lkwargs, rvargs, rkwargs = \
                    parse_subargs(s[0], s[1:], gvars)
                for lvarg in lvargs:
                    _print(getattr(lvarg, "max")(*rvargs, **rkwargs))

        if self.targs.min:
            for min_arg in self.targs.min:
                s = min_arg.split("$")
                lvargs, lkwargs, rvargs, rkwargs = \
                    parse_subargs(s[0], s[1:], gvars)
                for lvarg in lvargs:
                    _print(getattr(lvarg, "min")(*rvargs, **rkwargs))

        if self.targs.mean:
            for mean_arg in self.targs.mean:
                s = mean_arg.split("$")
                lvargs, lkwargs, rvargs, rkwargs = \
                    parse_subargs(s[0], s[1:], gvars)
                for lvarg in lvargs:
                    _print(getattr(lvarg, "mean")(*rvargs, **rkwargs))

        if self.targs.std:
            for std_arg in self.targs.std:
                s = std_arg.split("$")
                lvargs, lkwargs, rvargs, rkwargs = \
                    parse_subargs(s[0], s[1:], gvars)
                for lvarg in lvargs:
                    _print(getattr(lvarg, "std")(*rvargs, **rkwargs))

        if self.targs.str:
            for str_arg in self.targs.str:
                s = str_arg.split("$")
                vargs, kwargs = funcargs_eval(s[0], s[1:], gvars)
                for varg in vargs:
                    _print(varg)
        elif not printed:
            if isinstance(gvars["D"], list):
                for d in gvars["D"]:
                    _print(d)
            elif gvars["D"] is not None:
                _print(gvars["D"])

