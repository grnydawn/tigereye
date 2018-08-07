# -*- coding: utf-8 -*-
"entry task handling module."

import argparse
import string

from .error import UsageError
from .util import teval, parse_optionvalue
from .builtin import builtin_tasks

def parse_global_opts(argv, gopts, tasks, default_task, desc):

    # parse global options
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('command', nargs='?', help='input data.')
    parser.add_argument('data', nargs='*', help='input data.')

    handlers = {}

    for handler, vargs, kwargs in gopts:
        parser.add_argument(*vargs, **kwargs)
        handlers[parser._actions[-1].dest] = handler

    # split global and task options
    global_argv = []
    task_argv = []

    for idx, arg in enumerate(argv):
        if arg == "--":
            task_argv.extend(argv[idx:])
            break
        else:
            global_argv.append(arg)

    # parse global options
    gargs, command_argv = parser.parse_known_args(global_argv)

    if gargs.command:
        if gargs.command in tasks.keys():
            first_task = gargs.command
        else:
            gargs.data.insert(0, gargs.command)
            first_task = default_task
        gargs.command = None
    else:
        first_task = default_task

    # recover task options if any
    #if gargs.data[0] in tasks.keys():
    #    first_task = gargs.data.pop(0)
    #else:
    #    first_task = default_task

    command_argv.insert(0, first_task)
    task_argv = command_argv + task_argv

    return gargs, task_argv, handlers

def entry_task(argv, gopts, gvars, tasks, default_task, desc):

    gargs, task_argv, handlers = parse_global_opts(argv, gopts, tasks, default_task, desc)

    # handle builtin commands
    if gargs.command and gargs.command in builtin_tasks:
        import pdb; pdb.set_trace()

    # handle data argument 

    if gargs.data:
        gvars["D"] = []
        for d in gargs.data:
            s = d.split("$")
            gvars["D"].append(teval(s[0], s[1:], gvars))

    # handle user-provided options

    for opt_name, handler in handlers.items():
       if handler and hasattr(gargs, opt_name):
            optval = getattr(gargs, opt_name)
            if optval:

                s = optval.split("$")
                items, vargs, kwargs = parse_optionvalue('r'+s[0], s[1:], gvars)

                out = handler(items, vargs, kwargs)
                for k, v in out.items():
                    gvars["A"][k] = v

    # load inputs
    #teye_data_load(gargs, gvars)

    return task_argv

