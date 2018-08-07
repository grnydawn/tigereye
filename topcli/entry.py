# -*- coding: utf-8 -*-
"entry task handling module."

import argparse

from .error import UsageError
from .util import teval, parse_optionvalue
from .builtin import builtin_tasks

def parse_app_opts(argv, gopts, tasks, default_task, desc):

    # parse application options
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('command', nargs='?', help='subcommand')
    parser.add_argument('data', nargs='*', help='input data.')

    handlers = {}

    for handler, vargs, kwargs in gopts:
        parser.add_argument(*vargs, **kwargs)
        handlers[parser._actions[-1].dest] = handler

    # split global and task options
    app_argv = []
    task_argv = []

    for idx, arg in enumerate(argv):
        if arg == "--":
            task_argv.extend(argv[idx:])
            break
        else:
            app_argv.append(arg)

    # parse global options
    app_args, command_argv = parser.parse_known_args(app_argv)

    if app_args.command:
        if app_args.command in tasks.keys():
            first_task = app_args.command
        else:
            app_args.data.insert(0, app_args.command)
            first_task = default_task
        app_args.command = None
    else:
        first_task = default_task

    # recover task options if any
    #if gargs.data[0] in tasks.keys():
    #    first_task = gargs.data.pop(0)
    #else:
    #    first_task = default_task

    command_argv.insert(0, first_task)
    task_argv = command_argv + task_argv

    return app_args, task_argv, handlers

def entry_task(argv, gopts, app_vars, tasks, default_task, desc):

    app_args, task_argv, handlers = parse_app_opts(argv, gopts, tasks, default_task, desc)

    # handle builtin commands
    if app_args.command and app_args.command in builtin_tasks:
        import pdb; pdb.set_trace()

    # handle data argument 

    if app_args.data:
        app_vars["D"] = []
        for d in app_args.data:
            s = d.split("$")
            app_vars["D"].append(teval(s[0], s[1:], app_vars))

    # handle user-provided options

    for opt_name, handler in handlers.items():
       if handler and hasattr(app_args, opt_name):
            optval = getattr(app_args, opt_name)
            if optval:

                s = optval.split("$")
                items, vargs, kwargs = parse_optionvalue('r'+s[0], s[1:], app_vars)

                out = handler(items, vargs, kwargs)
                for k, v in out.items():
                    app_vars[k] = v

    # load inputs
    #teye_data_load(gargs, gvars)

    return task_argv

