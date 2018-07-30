# -*- coding: utf-8 -*-
"tigereye verify core task module."

import os
import argparse

from ..task import Task
from ..error import UsageError
from ..util import teval, funcargs_eval, parse_optionvalue

class verify_task(Task):

    def __init__(self, targv):

        self.parser.add_argument("-t", '--test', metavar='test', action='append', help='testing)')
        self.parser.add_argument("-p", '--onpass', metavar='pass', action='append', help='on pass)')
        self.parser.add_argument("-f", '--onfail', metavar='fail', action='append', help='on fail)')
        self.parser.add_argument("-e", '--onerror', metavar='error', action='append', help='on error)')
        self.parser.add_argument('--version', action='version', version='tigereye verifying task version 0.0.0')

        self.targs = self.parser.parse_args(targv)

    def _call(self, gvars, *vargs, **kwargs):
        import pdb; pdb.set_trace()

    def _print(self, gvars, *vargs, **kwargs):
        for varg in vargs:
            print(varg+"\n")

    def perform(self, gvars):

        verified = set()
        tests = {}

        def _get_results(vargs):
            if len(vargs) > 1:
                results = vargs
            elif len(vargs) == 1:
                results = vargs[0]
            else:
                results = None
            return results

        def _print_result(tname, res):
            if res == True:
                print("Test '%s' is passed."%tname)
            elif res == False:
                print("Test '%s' is failed."%tname)
            elif res == None:
                print("Test '%s' is not performed correctly."%tname)
            else:
                raise UsageError("Test is not correct.")

        if self.targs.test:
            for idx, test_arg in enumerate(self.targs.test):
                s = test_arg.split("$")
                split_arg = s[0].split("@")
                # syntax: [testname@]test
                try:
                    if len(split_arg) == 1:
                        tests['test%d'%idx] = None
                        vargs, kwargs = funcargs_eval(s[0], s[1:], gvars)
                        tests['test%d'%idx] = _get_results(vargs)
                    elif len(split_arg) == 2:
                        tests[split_arg[0].strip()] = None
                        vargs, kwargs = funcargs_eval(split_arg[1], s[1:], gvars)
                        tests[split_arg[0].strip()] = _get_results(vargs)
                except Exception as err:
                    pass

        gvars.update(tests)

        if self.targs.onerror:
            for error_arg in self.targs.onerror:
                s = error_arg.split("$")

                # syntax: [testname[, testname...]@]funcname@funcargs
                # text, varmap, gvars, evals
                items, vargs, kwargs = parse_optionvalue(s[0], s[1:], gvars)

                if len(items) == 1:
                    tests = ["test0"]
                    action = items[0][0][0]
                elif len(items) == 2:
                    tests = items[0][0]
                    action = items[1][0][0]
                else:
                    UsageError("Following option needs one or two items at the left of @: %s"%error_arg)

                for test in tests:
                    if gvars[test] == None:
                        getattr(self, "_"+action)(gvars, *vargs, **kwargs)
                        verified.add(True)

        if self.targs.onfail:
            for fail_arg in self.targs.onfail:
                s = fail_arg.split("$")

                # syntax: [testname[, testname...]@]funcname@funcargs
                # text, varmap, gvars, evals
                items, vargs, kwargs = parse_optionvalue(s[0], s[1:], gvars)

                if len(items) == 1:
                    tests = ["test0"]
                    action = items[0][0][0]
                elif len(items) == 2:
                    tests = items[0][0]
                    action = items[1][0][0]
                else:
                    UsageError("Following option needs one or two items at the left of @: %s"%fail_arg)

                for test in tests:
                    if gvars[test] == False:
                        getattr(self, "_"+action)(gvars, *vargs, **kwargs)
                        verified.add(True)


        if self.targs.onpass:
            for pass_arg in self.targs.onpass:
                s = pass_arg.split("$")

                # syntax: [testname[, testname...]@]funcname@funcargs
                # text, varmap, gvars, evals
                items, vargs, kwargs = parse_optionvalue(s[0], s[1:], gvars)

                if len(items) == 1:
                    tests = ["test0"]
                    action = items[0][0][0]
                elif len(items) == 2:
                    tests = items[0][0]
                    action = items[1][0][0]
                else:
                    UsageError("Following option needs one or two items at the left of @: %s"%pass_arg)

                for test in tests:
                    if gvars[test] == True:
                        getattr(self, "_"+action)(gvars, *vargs, **kwargs)
                        verified.add(True)

        if not verified:
            for tname, results in tests.items():
                if isinstance(results, list):
                    for res in results:
                        _print_result(tname, res)
                else:
                    _print_result(tname, results)

