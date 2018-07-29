# -*- coding: utf-8 -*-
"tigereye clean core task module."

import os
import argparse

from ..task import Task
from ..error import UsageError
from ..util import teval, funcargs_eval, parse_subargs

class clean_task(Task):

    def __init__(self, targv):

        parser = argparse.ArgumentParser(description='tigereye cleaning task')
        parser.add_argument("-i", '--inspect', metavar='inspect', action='append', help='inspection)')
        parser.add_argument('--calc', metavar='calc', action='append', help='python code for manipulating data.')
        parser.add_argument('--import-task', metavar='task', action='append', help='import task')
        parser.add_argument('--import-function', metavar='function', action='append', help='import function')
        parser.add_argument('--output', metavar='output', action='append', help='output variable.')
        parser.add_argument('--name', metavar='task name', help='task name')
        parser.add_argument('--version', action='version', version='tigereye verifying task version 0.0.0')

        self.targs = parser.parse_args(targv)

    def _call(self, action, gvars):
        import pdb; pdb.set_trace()

    def _print(self, action, gvars):
        print(teval(action, [], gvars))

    def perform(self, gvars):

        if self.targs.inspect:
            for idx, inspect_arg in enumerate(self.targs.inspect):
                s = test_arg.split("$")
                split_arg = s[0].split("@")

                try:
                    if len(split_arg) == 1:
                        tests['inspect%d'%idx] = None
                        vargs, kwargs = funcargs_eval(s[0], s[1:], gvars)
                        tests['inspect%d'%idx] = _get_results(vargs)
                    elif len(split_arg) == 2:
                        tests[split_arg[0].strip()] = None
                        vargs, kwargs = funcargs_eval(split_arg[1], s[1:], gvars)
                        tests[split_arg[0].strip()] = _get_results(vargs)
                except Exception as err:
                    pass

#        verified = set()
#        tests = {}
#
#        def _get_results(vargs):
#            if len(vargs) > 1:
#                results = vargs
#            elif len(vargs) == 1:
#                results = vargs[0]
#            else:
#                results = None
#            return results
#
#        def _print_result(tname, res):
#            if res == True:
#                print("Test '%s' is passed."%tname)
#            elif res == False:
#                print("Test '%s' is failed."%tname)
#            elif res == None:
#                print("Test '%s' is not performed correctly."%tname)
#            else:
#                raise UsageError("Test is not correct.")
#
#        if self.targs.test:
#            for idx, test_arg in enumerate(self.targs.test):
#                s = test_arg.split("$")
#                split_arg = s[0].split("@")
#
#                try:
#                    if len(split_arg) == 1:
#                        tests['test%d'%idx] = None
#                        vargs, kwargs = funcargs_eval(s[0], s[1:], gvars)
#                        tests['test%d'%idx] = _get_results(vargs)
#                    elif len(split_arg) == 2:
#                        tests[split_arg[0].strip()] = None
#                        vargs, kwargs = funcargs_eval(split_arg[1], s[1:], gvars)
#                        tests[split_arg[0].strip()] = _get_results(vargs)
#                except Exception as err:
#                    pass
#
#        gvars.update(tests)
#
#        if self.targs.onerror:
#            for fail_arg in self.targs.onerror:
#                s = fail_arg.split("$")
#                head, action = s[0].split("@")
#                split_head = head.split(",")
#
#                if len(split_head) == 1:
#                    testname = "test0"
#                    actiontype = split_head[0].strip()
#                elif len(split_head) == 2:
#                    testname = split_head[0].strip()
#                    actiontype = split_head[1].strip()
#
#                if gvars[testname] == None:
#                    getattr(self, "_"+actiontype)(action.strip(), gvars)
#                    verified.add(True)
#
#        if self.targs.onfail:
#            for fail_arg in self.targs.onfail:
#                s = fail_arg.split("$")
#                head, action = s[0].split("@")
#                split_head = head.split(",")
#
#                if len(split_head) == 1:
#                    testname = "test0"
#                    actiontype = split_head[0].strip()
#                elif len(split_head) == 2:
#                    testname = split_head[0].strip()
#                    actiontype = split_head[1].strip()
#
#                if gvars[testname] == False:
#                    getattr(self, "_"+actiontype)(action.strip(), gvars)
#                    verified.add(True)
#
#        if self.targs.onpass:
#            for pass_arg in self.targs.onpass:
#                s = pass_arg.split("$")
#                head, action = s[0].split("@")
#                split_head = head.split(",")
#
#                if len(split_head) == 1:
#                    testname = "test0"
#                    actiontype = split_head[0].strip()
#                elif len(split_head) == 2:
#                    testname = split_head[0].strip()
#                    actiontype = split_head[1].strip()
#
#                if gvars[testname] == True:
#                    getattr(self, "_"+actiontype)(action.strip(), gvars)
#                    verified.add(True)
#
#        if not verified:
#            for tname, results in tests.items():
#                if isinstance(results, list):
#                    for res in results:
#                        _print_result(tname, res)
#                else:
#                    _print_result(tname, results)
#
