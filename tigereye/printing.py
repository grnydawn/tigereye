# -*- coding: utf-8 -*-
"tigereye print core task module."

import os
import argparse

from topcli import Task, UsageError, funcargs_eval, parse_optionvalue

class print_task(Task):

    def __init__(self, targv):

        self.parser.add_argument("-s", '--str', metavar='str', action='append', help='run str()')
        self.parser.add_argument('--shape', metavar='data shape', action='append', help='data shape')
        self.parser.add_argument('--ndim', metavar='data dimension', action='append', help='data dimension')
        self.parser.add_argument('--head', metavar='data head', action='append', help='data head')
        self.parser.add_argument('--tail', metavar='data tail', action='append', help='data tail')
        self.parser.add_argument('--dtypes', metavar='data types', action='append', help='data types')
        self.parser.add_argument('--describe', metavar='data description', action='append', help='data description')
        self.parser.add_argument('--count', metavar='element count', action='append', help='data element count')
        self.parser.add_argument('--max', metavar='max value', action='append', help='maximum element')
        self.parser.add_argument('--min', metavar='min value', action='append', help='minimum element')
        self.parser.add_argument('--mean', metavar='mean value', action='append', help='mean value')
        self.parser.add_argument('--std', metavar='std value', action='append', help='standard deviation value')
        self.parser.add_argument('--version', action='version', version='tigereye printing task version 0.0.0')

        self.targs = self.parser.parse_args(targv)

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

                # syntax: data[,data...][@funcargs]
                # text, varmap, gvars, evals
                items, vargs, kwargs = parse_optionvalue(s[0], s[1:], gvars, evals=[True])

                if len(items) == 0:
                    data = vargs
                    vargs = []
                elif len(items) == 1:
                    data = items[0][0]
                else:
                    UsageError("The synaxt error near '@': %s"%tail_arg)

                for d in data:
                    _print(getattr(d, "tail")(*vargs, **kwargs))

        if self.targs.tail:
            for tail_arg in self.targs.tail:
                s = tail_arg.split("$")

                # syntax: data[,data...][@funcargs]
                # text, varmap, gvars, evals
                items, vargs, kwargs = parse_optionvalue(s[0], s[1:], gvars, evals=[True])

                if len(items) == 0:
                    data = vargs
                    vargs = []
                elif len(items) == 1:
                    data = items[0][0]
                else:
                    UsageError("The synaxt error near '@': %s"%head_arg)

                for d in data:
                    _print(getattr(d, "head")(*vargs, **kwargs))

        if self.targs.describe:
            for describe_arg in self.targs.describe:
                s = describe_arg.split("$")

                # syntax: data[,data...][@funcargs]
                # text, varmap, gvars, evals
                items, vargs, kwargs = parse_optionvalue(s[0], s[1:], gvars, evals=[True])

                if len(items) == 0:
                    data = vargs
                    vargs = []
                elif len(items) == 1:
                    data = items[0][0]
                else:
                    UsageError("The synaxt error near '@': %s"%describe_arg)

                for d in data:
                    _print(getattr(d, "describe")(*vargs, **kwargs))

        if self.targs.count:
            for count_arg in self.targs.count:
                s = count_arg.split("$")

                # syntax: data[,data...][@funcargs]
                # text, varmap, gvars, evals
                items, vargs, kwargs = parse_optionvalue(s[0], s[1:], gvars, evals=[True])

                if len(items) == 0:
                    data = vargs
                    vargs = []
                elif len(items) == 1:
                    data = items[0][0]
                else:
                    UsageError("The synaxt error near '@': %s"%count_arg)

                for d in data:
                    _print(getattr(d, "count")(*vargs, **kwargs))

        if self.targs.max:
            for max_arg in self.targs.max:
                s = max_arg.split("$")

                # syntax: data[,data...][@funcargs]
                # text, varmap, gvars, evals
                items, vargs, kwargs = parse_optionvalue(s[0], s[1:], gvars, evals=[True])

                if len(items) == 0:
                    data = vargs
                    vargs = []
                elif len(items) == 1:
                    data = items[0][0]
                else:
                    UsageError("The synaxt error near '@': %s"%max_arg)

                for d in data:
                    _print(getattr(d, "max")(*vargs, **kwargs))

        if self.targs.min:
            for min_arg in self.targs.min:
                s = min_arg.split("$")

                # syntax: data[,data...][@funcargs]
                # text, varmap, gvars, evals
                items, vargs, kwargs = parse_optionvalue(s[0], s[1:], gvars, evals=[True])

                if len(items) == 0:
                    data = vargs
                    vargs = []
                elif len(items) == 1:
                    data = items[0][0]
                else:
                    UsageError("The synaxt error near '@': %s"%min_arg)

                for d in data:
                    _print(getattr(d, "min")(*vargs, **kwargs))

        if self.targs.mean:
            for mean_arg in self.targs.mean:
                s = mean_arg.split("$")

                # syntax: data[,data...][@funcargs]
                # text, varmap, gvars, evals
                items, vargs, kwargs = parse_optionvalue(s[0], s[1:], gvars, evals=[True])

                if len(items) == 0:
                    data = vargs
                    vargs = []
                elif len(items) == 1:
                    data = items[0][0]
                else:
                    UsageError("The synaxt error near '@': %s"%mean_arg)

                for d in data:
                    _print(getattr(d, "mean")(*vargs, **kwargs))

        if self.targs.std:
            for std_arg in self.targs.std:
                s = std_arg.split("$")

                # syntax: data[,data...][@funcargs]
                # text, varmap, gvars, evals
                items, vargs, kwargs = parse_optionvalue(s[0], s[1:], gvars, evals=[True])

                if len(items) == 0:
                    data = vargs
                    vargs = []
                elif len(items) == 1:
                    data = items[0][0]
                else:
                    UsageError("The synaxt error near '@': %s"%std_arg)

                for d in data:
                    _print(getattr(d, "std")(*vargs, **kwargs))

        if self.targs.str:
            for str_arg in self.targs.str:
                s = str_arg.split("$")
                vargs, kwargs = funcargs_eval(s[0], s[1:], gvars)
                for varg in vargs:
                    _print(varg)
        elif not printed:
            for d in gvars["D"]:
                _print(d)

