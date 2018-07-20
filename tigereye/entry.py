# -*- coding: utf-8 -*-
"entry task handling module."

import argparse

from .util import error_exit

try:
    import numpy
    import matplotlib
    import pandas
except ImportError as err:
    error_exit(err)

from .core_tasks import tasks
from .load import teye_data_load

default_task = 'plot'

def handle_global_options(gargs, gvars):

    if gargs.pdf_bind:
        from matplotlib.backends.backend_pdf import PdfPages
        attrs['B'] =  teval('_p(%s)'%gargs.pdf_bind, gvars, _p=PdfPages)

def teye_entry_task(argv, gvars):

    # parse global options
    parser = argparse.ArgumentParser(description='All-in-one data utility.')
    parser.add_argument('data', metavar='input data', nargs='+', help='input data.')
    parser.add_argument('--data-format', action="append", help='input data format.')
    parser.add_argument('--pdf-bind', help='generate pdf binding.')

    # split global and task options
    global_argv = []
    task_argv = []

    for idx, arg in enumerate(argv):
        if arg == "->":
            task_argv.extend(argv[idx+1:])
            break
        else:
            global_argv.append(arg)

    # parse global options
    gargs, command_argv = parser.parse_known_args(global_argv)

    # recover task options if any
    if gargs.data[0] in tasks.keys():
        first_task = gargs.data.pop(0)
        task_argv.insert(0, first_task)
        task_argv.insert(1, "->")

    if task_argv:
        if task_argv[0] not in tasks.keys():
            task_argv.insert(0, default_task)
    elif gargs.data:
        task_argv.append(default_task)

    # import numpy, pandas, and matplotlib
    gvars['numpy'] = gvars['np'] = numpy
    gvars['pandas'] = gvars['pd'] = pandas
    gvars['matplotlib'] = gvars['mpl'] = matplotlib

    # load inputs
    teye_data_load(gargs, gvars)

    # handling remaining global options
    handle_global_options(gargs, gvars)

    # return remaining arguments
    return task_argv
