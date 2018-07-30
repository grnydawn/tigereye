# -*- coding: utf-8 -*-
"tigereye plot core task module."

import os
import argparse

from ..task import Task
from ..error import UsageError
from ..util import funcargs_eval, parse_optionvalue, error_exit

class plot_task(Task):

    def __init__(self, targv):

        self.parser.add_argument('-f', metavar='figure creation', help='define a figure for plotting.')
        self.parser.add_argument('-t', '--title', metavar='title', action='append', help='title  plotting.')
        self.parser.add_argument('-p', '--plot', metavar='plot type', action='append', help='plot type for plotting.')
        self.parser.add_argument('-s', '--save', metavar='save', action='append', help='file path to save png image.')
        self.parser.add_argument('-x', '--xaxis', metavar='xaxis', action='append', help='axes function wrapper for x axis settings.')
        self.parser.add_argument('-y', '--yaxis', metavar='yaxis', action='append', help='axes function wrapper for y axis settings.')
        self.parser.add_argument('-z', '--zaxis', metavar='zaxis', action='append', help='axes function wrapper for z axis settings.')
        self.parser.add_argument('-g', action='store_true', help='grid for ax plotting.')
        self.parser.add_argument('-l', action='store_true', help='legend for ax plotting')
        self.parser.add_argument('--pandas', metavar='pandas', action='append', help='pandas plots.')
        self.parser.add_argument('--pages', metavar='pages', help='page settings.')
        self.parser.add_argument('--page-calc', metavar='page_calc', action='append', help='python code for manipulating data within page generation.')
        self.parser.add_argument('--legend', metavar='legend', action='append', help='plot legend')
        self.parser.add_argument('--grid', metavar='grid', action='append', help='grid for plotting.')
        self.parser.add_argument('--subplot', metavar='subplot', action='append', help='define subplot.')
        self.parser.add_argument('--figure', metavar='figure function', action='append', help='define Figure function.')
        self.parser.add_argument('--axes', metavar='axes', action='append', help='define Axes function.')
        self.parser.add_argument('--noshow', action='store_true', default=False, help='prevent showing plot on screen.')
        self.parser.add_argument('--noplot', action='store_true', default=False, help='prevent generating plot.')
        self.parser.add_argument('--version', action='version', version='tigereye plotting task version 0.0.0')

        self.targs = self.parser.parse_args(targv)

    def perform(self, gvars):

        # pages setting
        if self.targs.pages:
            s = self.targs.pages.split("$")
            vargs, kwargs = funcargs_eval(s[0], s[1:], gvars)

            if vargs:
                gvars['num_pages'] = vargs[-1]
            else:
                gvars['num_pages'] = 1

            for key, value in kwargs.items():
                gvars[key] = value
        else:
            gvars['num_pages'] = 1

        # page iteration
        for idx in range(gvars['num_pages']):

            gvars['page_num'] = idx

            if self.targs.page_calc:
                for page_calc in self.targs.page_calc:
                    s = page_calc.split("$")
                    vargs, kwargs = funcargs_eval(s[0], s[1:], gvars)
                    gvars.update(kwargs)

            # figure setting
            if self.targs.f:
                s = self.targs.f.split("$")
                gvars['figure'] = teval('pyplot.figure(%s)'%s[0], s[1:], gvars)
            else:
                gvars['figure'] = gvars['pyplot'].figure()

            # plot axis
            if self.targs.subplot:
                for subplot_arg in self.targs.subplot:
                    # split by $; apply variable mapping repeatedly
                    s = subplot_arg.split("$")

                    # syntax: subplotname@funcargs
                    # text, varmap, gvars, evals
                    items, vargs, kwargs = parse_optionvalue(s[0], s[1:], gvars)

                    if len(items) == 1:
                        subpname = items[0][0][0]

                        if 'projection' in kwargs and kwargs['projection'] == '3d':
                             from mpl_toolkits.mplot3d import Axes3D
                             gvars['Axes3D'] = Axes3D
                        if vargs:
                            gvars[subpname] = gvars['figure'].add_subplot(*vargs, **kwargs)
                        else:
                            gvars[subpname] = gvars['figure'].add_subplot(111, **kwargs)
                    else:
                        UsageError("The synaxt error near '@': %s"%subplot_arg)

            # page names
            if 'page_names' in gvars:
                page_names = gvars['page_names']
                if callable(page_names):
                    gvars['page_name'] = page_names(gvars['page_num'])
                else:
                    gvars['page_name'] = page_names[gvars['page_num']]
            else:
                gvars['page_name'] = 'page%d'%gvars['page_num']

            # execute figure functions
            if self.targs.figure:
                for fig_arg in self.targs.figure:
                    s = fig_arg.split("$")

                    # syntax: funcname@funcargs
                    # text, varmap, gvars, evals
                    items, vargs, kwargs = parse_optionvalue(s[0], s[1:], gvars)

                    if len(items) == 1:
                        funcname = items[0][0][0]
                    else:
                        UsageError("The synaxt error near '@': %s"%fig_arg)

                    getattr(gvars['figure'], funcname)(*vargs, **kwargs)

            if self.targs.pandas:
                s = self.targs.pandas.split("$")
                pandas_args = s[0].split("@")
                if len(pandas_args) == 1:
                    gvars["ax"] = teval(pandas_args[0], s[1:], gvars)
                elif len(pandas_args) == 2:
                    gvars[pandas_args[0].strip()] = teval(pandas_args[1], s[1:], gvars)
                else:
                    raise UsageError("pandas option has wrong syntax on using '@': %s"%self.targs.pandas)

            elif not self.targs.subplot:
                gvars['ax'] = gvars['figure'].add_subplot(111)

            # plotting
            plots = []
            if self.targs.plot:
                for plot_arg in self.targs.plot:
                    s = plot_arg.split("$")

                    # syntax: [axname[, axname...]@]funcname@funcargs
                    # text, varmap, gvars, evals
                    items, vargs, kwargs = parse_optionvalue(s[0], s[1:], gvars, evals=[True, False])

                    if len(items) == 1:
                        axes = [gvars["ax"]]
                        funcname = items[0][0][0]
                    elif len(items) == 2:
                        axes = items[0][0]
                        funcname = items[1][0][0]
                    else:
                        UsageError("Following option needs one or two items at the left of @: %s"%plot_arg)

                    for ax in axes:
                        if hasattr(ax, funcname):
                            plot_handle = getattr(ax, funcname)(*vargs, **kwargs)

                            try:
                                for p in plot_handle:
                                    plots.append(p)
                            except TypeError:
                                plots.append(plot_handle)
                        else:
                            # TODO: handling this case
                            pass

                    if funcname == 'pie':
                        for ax in axes:
                            gvars[ax].axis('equal')

            if 'plots' in gvars:
                gvars['plots'].extend(plots)
            else:
                gvars['plots'] = plots

            # title setting
            if self.targs.title:
                for title_arg in self.targs.title:
                    s = title_arg.split("$")

                    # syntax: [axname[,axname...]@]funcargs
                    # text, varmap, gvars, evals
                    items, vargs, kwargs = parse_optionvalue(s[0], s[1:], gvars, evals=[True])

                    if len(items) == 0:
                        axes = [gvars["ax"]]
                    elif len(items) == 1:
                        axes = items[0][0]
                    else:
                        UsageError("The synaxt error near '@': %s"%title_arg)

                    for ax in axes:
                        ax.set_title(*vargs, **kwargs)

            # x-axis setting
            if self.targs.xaxis:
                for xaxis_arg in self.targs.xaxis:
                    s = xaxis_arg.split("$")

                    # syntax: [axname[, axname...]@]funcname@funcargs
                    # text, varmap, gvars, evals
                    items, vargs, kwargs = parse_optionvalue(s[0], s[1:], gvars, evals=[True, False])

                    if len(items) == 1:
                        axes = [gvars["ax"]]
                        funcname = "set_x"+items[0][0][0]
                    elif len(items) == 2:
                        axes = items[0][0]
                        funcname = "set_x"+items[1][0][0]
                    else:
                        UsageError("Following option needs one or two items at the left of @: %s"%xaxis_arg)

                    for ax in axes:
                        if hasattr(ax, funcname):
                            getattr(ax, funcname)(*vargs, **kwargs)
                        else:
                            # TODO: handling this case
                            pass

           # y-axis setting
            if self.targs.yaxis:
                for yaxis_arg in self.targs.yaxis:
                    s = yaxis_arg.split("$")

                    # syntax: [axname[, axname...]@]funcname@funcargs
                    # text, varmap, gvars, evals
                    items, vargs, kwargs = parse_optionvalue(s[0], s[1:], gvars, evals=[True, False])

                    if len(items) == 1:
                        axes = [gvars["ax"]]
                        funcname = "set_y"+items[0][0][0]
                    elif len(items) == 2:
                        axes = items[0][0]
                        funcname = "set_y"+items[1][0][0]
                    else:
                        UsageError("Following option needs one or two items at the left of @: %s"%yaxis_arg)

                    for ax in axes:
                        if hasattr(ax, funcname):
                            getattr(ax, funcname)(*vargs, **kwargs)
                        else:
                            # TODO: handling this case
                            pass

            # z-axis setting
            if self.targs.zaxis:
                for zaxis_arg in self.targs.zaxis:
                    s = zaxis_arg.split("$")

                    # syntax: [axname[, axname...]@]funcname@funcargs
                    # text, varmap, gvars, evals
                    items, vargs, kwargs = parse_optionvalue(s[0], s[1:], gvars, evals=[True, False])

                    if len(items) == 1:
                        axes = [gvars["ax"]]
                        funcname = "set_z"+items[0][0][0]
                    elif len(items) == 2:
                        axes = items[0][0]
                        funcname = "set_z"+items[1][0][0]
                    else:
                        UsageError("Following option needs one or two items at the left of @: %s"%zaxis_arg)

                    for ax in axes:
                        if hasattr(ax, funcname):
                            getattr(ax, funcname)(*vargs, **kwargs)
                        else:
                            # TODO: handling this case
                            pass

            # grid setting
            if self.targs.g:
                for key, value in gvars.items():
                    if isinstance(value, gvars['mpl'].axes.Axes):
                        value.grid()

            if self.targs.grid:
                for grid_arg in self.targs.grid:
                    s = grid_arg.split("$")

                    # syntax: [axname[,axname...]@]funcargs
                    # text, varmap, gvars, evals
                    items, vargs, kwargs = parse_optionvalue(s[0], s[1:], gvars, evals=[True])

                    if len(items) == 0:
                        axes = [gvars["ax"]]
                    elif len(items) == 1:
                        axes = items[0][0]
                    else:
                        UsageError("The synaxt error near '@': %s"%grid_arg)

                    for ax in axes:
                        ax.grid(*vargs, **kwargs)

            # legend setting
            if self.targs.l:
                for key, value in gvars.items():
                    if isinstance(value, gvars['mpl'].axes.Axes):
                        value.legend()

            if self.targs.legend:
                for legend_arg in self.targs.legend:
                    s = legend_arg.split("$")

                    # syntax: [axname[,axname...]@]funcargs
                    # text, varmap, gvars, evals
                    items, vargs, kwargs = parse_optionvalue(s[0], s[1:], gvars, evals=[True])

                    if len(items) == 0:
                        axes = [gvars["ax"]]
                    elif len(items) == 1:
                        axes = items[0][0]
                    else:
                        UsageError("The synaxt error near '@': %s"%legend_arg)

                    for ax in axes:
                        ax.legend(*vargs, **kwargs)

            # execute axes functions
            if self.targs.axes:
                for axes_arg in self.targs.axes:
                    s = axes_arg.split("$")
                    # syntax: [axname[, axname...]@]funcname@funcargs
                    # text, varmap, gvars, evals
                    items, vargs, kwargs = parse_optionvalue(s[0], s[1:], gvars, evals=[True, False])

                    if len(items) == 1:
                        axes = [gvars["ax"]]
                        funcname = items[0][0][0]
                    elif len(items) == 2:
                        axes = items[0][0]
                        funcname = items[1][0][0]
                    else:
                        UsageError("Following option needs one or two items at the left of @: %s"%axes_arg)

                    for ax in axes:
                        getattr(ax, funcname)(*vargs, **kwargs)

            elif not gvars['plots']:
                if self.targs.figure:
                    pass
                elif gvars["D"] is not None:
                    if isinstance(gvars["D"], list):
                        for data_obj in gvars['D']:
                            data_obj.plot()
                    else:
                        gvars["D"].plot()
                else:
                    error_exit("There is no data to plot.")

            # saving an image file
            if self.targs.save:
                for save_arg in self.targs.save:
                    s = save_arg.split("$")
                    # savefig(fname, dpi=None, facecolor='w', edgecolor='w',
                    # orientation='portrait', papertype=None, format=None,
                    # transparent=False, bbox_inches=None, pad_inches=0.1,
                    # frameon=None)
                    # syntax: funcargs
                    # text, varmap, gvars, evals
                    items, vargs, kwargs = parse_optionvalue('r'+s[0], s[1:], gvars)

                    name = vargs.pop(0)

                    if gvars['num_pages'] > 1:
                        root, ext = os.path.splitext(name)
                        name = '%s-%d%s'%(root, gvars['page_num'], ext)

                    gvars["figure"].savefig(name, *vargs, **kwargs)

            if gvars["B"]:
                gvars["B"].savefig(figure=gvars["figure"])

            # displyaing an image on screen
            if not self.targs.noshow:
                gvars['pyplot'].show()

            gvars["figure"].clear()
            gvars["pyplot"].close(gvars["figure"])
            del gvars['figure']
