# -*- coding: utf-8 -*-
"entry task handling module."

import argparse

from .util import error_exit, parse_optionvalue

try:
    import numpy
    import matplotlib
    import matplotlib.pyplot
    import pandas
except ImportError as err:
    error_exit(err)

from .core_tasks import tasks
from .load import teye_data_load

default_task = 'plot'

def handle_global_options(gargs, gvars):

    if gargs.pdf_bind:

        s = gargs.pdf_bind.split("$")

        # syntax: funcargs
        # text, varmap, gvars, evals
        items, vargs, kwargs = parse_optionvalue('r'+s[0], s[1:], gvars)

        from matplotlib.backends.backend_pdf import PdfPages
        gvars["B"] = PdfPages(*vargs, **kwargs)

def parse_global_opts(argv):

    # parse global options
    parser = argparse.ArgumentParser(description='All-in-one data utility.')
    parser.add_argument('data', nargs='+', help='input data.')
    parser.add_argument('--data-format', action="append", help='input data format.')
    parser.add_argument('--pdf-bind', help='generate pdf binding.')
    parser.add_argument('--version',  action='version', version='tigereye version 0.2.1')

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

    # recover task options if any
    if gargs.data[0] in tasks.keys():
        first_task = gargs.data.pop(0)
    else:
        first_task = default_task

    command_argv.insert(0, first_task)
    task_argv = command_argv + task_argv

    return gargs, task_argv

def teye_entry_task(argv, gvars):

    gargs, task_argv = parse_global_opts(argv)

    # import numpy, pandas, and matplotlib
    gvars['numpy'] = gvars['np'] = numpy
    gvars['pandas'] = gvars['pd'] = pandas
    gvars['matplotlib'] = gvars['mpl'] = matplotlib
    gvars['pyplot'] = gvars['plt'] = matplotlib.pyplot

    # handling remaining global options
    handle_global_options(gargs, gvars)

    # load inputs
    teye_data_load(gargs, gvars)

    return task_argv

