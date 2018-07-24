# -*- coding: utf-8 -*-
"tigereye plot core task module."

import os
import argparse

from ..task import Task
from ..error import UsageError
from ..util import funcargs_eval, parse_subargs, error_exit

class plot_task(Task):

    def __init__(self, targv):

        parser = argparse.ArgumentParser(description='tigereye plotting task')
        parser.add_argument('-f', metavar='figure creation', help='define a figure for plotting.')
        parser.add_argument('-t', '--title', metavar='title', action='append', help='title  plotting.')
        parser.add_argument('-p', '--plot', metavar='plot type', action='append', help='plot type for plotting.')
        parser.add_argument('-s', '--save', metavar='save', action='append', help='file path to save png image.')
        parser.add_argument('-x', '--xaxis', metavar='xaxis', action='append', help='axes function wrapper for x axis settings.')
        parser.add_argument('-y', '--yaxis', metavar='yaxis', action='append', help='axes function wrapper for y axis settings.')
        parser.add_argument('-z', '--zaxis', metavar='zaxis', action='append', help='axes function wrapper for z axis settings.')
        parser.add_argument('-g', action='store_true', help='grid for ax plotting.')
        parser.add_argument('-l', action='store_true', help='legend for ax plotting')
        parser.add_argument('--import', metavar='import', action='append', help='import task')
        parser.add_argument('--name', metavar='task name', help='task name')
        parser.add_argument('--pandas', metavar='pandas', action='append', help='pandas plots.')
        parser.add_argument('--calc', metavar='calc', action='append', help='python code for manipulating data.')
        parser.add_argument('--pages', metavar='pages', help='page settings.')
        parser.add_argument('--page-calc', metavar='page_calc', action='append', help='python code for manipulating data within page generation.')
        parser.add_argument('--legend', metavar='legend', action='append', help='plot legend')
        parser.add_argument('--grid', metavar='grid', action='append', help='grid for plotting.')
        parser.add_argument('--ax', metavar='ax', action='append', help='define plot axes.')
        parser.add_argument('--figure', metavar='figure function', action='append', help='define Figure function.')
        parser.add_argument('--axes', metavar='axes', action='append', help='define Axes function.')
        parser.add_argument('--noshow', action='store_true', default=False, help='prevent showing plot on screen.')
        parser.add_argument('--noplot', action='store_true', default=False, help='prevent generating plot.')
        parser.add_argument('--version', action='version', version='tigereye plotting task version 0.0.0')

        self.parser = parser
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

        if self.targs.calc:
            for calc in self.targs.calc:
                s = calc.split("$")
                vargs, kwargs = funcargs_eval(s[0], s[1:], gvars)
                gvars.update(kwargs)

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
            if self.targs.ax:
                for ax_arg in self.targs.ax:
                    # split by $; apply variable mapping repeatedly
                    s = ax_arg.split("$")
                    lvargs, lkwargs, rvargs, rkwargs = \
                        parse_subargs(s[0], s[1:], gvars, left_eval=False)
                    for axname in lvargs:
                        if 'projection' in rkwargs and rkwargs['projection'] == '3d':
                             from mpl_toolkits.mplot3d import Axes3D
                             gvars['Axes3D'] = Axes3D
                        if rvargs:
                            gvars[axname] = gvars['figure'].add_subplot(rvargs[0], **rkwargs)
                        else:
                            gvars[axname] = gvars['figure'].add_subplot(111, **rkwargs)

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
                    lvargs, lkwargs, rvargs, rkwargs = \
                        parse_subargs(s[0], s[1:], gvars, left_eval=False)

                    for figfunc in lvargs:
                        getattr(gvars['figure'], figfunc)(*rvargs, **rkwargs)

            if self.targs.pandas:
                s = self.targs.pandas.split("$")
                pandas_args = s[0].split("@")
                if len(pandas_args) == 1:
                    gvars["ax"] = teval(pandas_args[0], s[1:], gvars)
                elif len(pandas_args) == 2:
                    gvars[pandas_args[0].strip()] = teval(pandas_args[1], s[1:], gvars)
                else:
                    raise UsageError("pandas option has wrong syntax on using '@': %s"%self.targs.pandas)

            elif not self.targs.ax:
                gvars['ax'] = gvars['figure'].add_subplot(111)

            # plotting
            plots = []
            #import pdb; pdb.set_trace()
            if self.targs.plot:
                for plot_arg in self.targs.plot:
                    s = plot_arg.split("$")
                    lvargs, lkwargs, rvargs, rkwargs = \
                        parse_subargs(s[0], s[1:], gvars, left_eval=False)

                    ##if not lvargs or not isinstance(gvars[lvargs[0]], gvars['mpl'].axes.Axes):

                    if len(lvargs) == 1:
                        ax = "ax"
                        funcname = lvargs[0]
                    elif len(lvargs) == 2:
                        ax = lvargs[0]
                        funcname = lvargs[1]
                    else:
                        UsageError("Following option needs one or two items at the left of @: %s"%xaxis_arg)

                    plot_handle = getattr(gvars[ax], funcname)(*rvargs, **rkwargs)

                    try:
                        for p in plot_handle:
                            plots.append(p)
                    except TypeError:
                        plots.append(plot_handle)

                    if funcname == 'pie':
                        gvars[ax].axis('equal')

            if 'plots' in gvars:
                gvars['plots'].extend(plots)
            else:
                gvars['plots'] = plots

            # title setting
            if self.targs.title:
                for title_arg in self.targs.title:
                    s = title_arg.split("$")
                    lvargs, lkwargs, rvargs, rkwargs = \
                        parse_subargs(s[0], s[1:], gvars)

                    if rvargs or rkwargs:
                        for ax in lvargs:
                            ax.set_title(*rvargs, **rkwargs)
                    elif lvargs or lkwargs:
                        gvars["ax"].set_title(*lvargs, **lkwargs)
                    else:
                        gvars["ax"].set_title()

            # x-axis setting
            if self.targs.xaxis:
                for xaxis_arg in self.targs.xaxis:
                    s = xaxis_arg.split("$")
                    lvargs, lkwargs, rvargs, rkwargs = \
                        parse_subargs(s[0], s[1:], gvars, left_eval=False)

                    if len(lvargs) == 1:
                        ax = "ax"
                        funcname = lvargs[0]
                    elif len(lvargs) == 2:
                        ax = lvargs[0]
                        funcname = lvargs[1]
                    else:
                        UsageError("Following option needs one or two items at the left of @: %s"%xaxis_arg)

                    set_xfuncs =  dict((x, getattr(gvars[ax], x)) for x in dir(gvars[ax]) if x.startswith('set_x'))

                    func = set_xfuncs.get("set_x"+funcname, None)
                    if func: 
                        func(*rvargs, **rkwargs)


            # y-axis setting
            if self.targs.yaxis:
                for yaxis_arg in self.targs.yaxis:
                    s = yaxis_arg.split("$")
                    lvargs, lkwargs, rvargs, rkwargs = \
                        parse_subargs(s[0], s[1:], gvars, left_eval=False)

                    if len(lvargs) == 1:
                        ax = "ax"
                        funcname = lvargs[0]
                    elif len(lvargs) == 2:
                        ax = lvargs[0]
                        funcname = lvargs[1]
                    else:
                        UsageError("Following option needs one or two items at the left of @: %s"%yaxis_arg)

                    set_yfuncs =  dict((y, getattr(gvars[ax], y)) for y in dir(gvars[ax]) if y.startswith('set_y'))

                    func = set_yfuncs.get("set_y"+funcname, None)
                    if func: 
                        func(*rvargs, **rkwargs)

            # z-axis setting
            if self.targs.zaxis:
                for zaxis_arg in self.targs.zaxis:
                    s = zaxis_arg.split("$")
                    lvargs, lkwargs, rvargs, rkwargs = \
                        parse_subargs(s[0], s[1:], gvars, left_eval=False)

                    if len(lvargs) == 1:
                        ax = "ax"
                        funcname = lvargs[0]
                    elif len(lvargs) == 2:
                        ax = lvargs[0]
                        funcname = lvargs[1]
                    else:
                        UsageError("Following option needs one or two items at the left of @: %s"%yaxis_arg)

                    set_zfuncs =  dict((z, getattr(gvars[ax], z)) for z in dir(gvars[ax]) if z.startswith('set_z'))

                    func = set_zfuncs.get("set_z"+funcname, None)
                    if func: 
                        func(*rvargs, **rkwargs)

            # grid setting
            if self.targs.g:
                for key, value in gvars.items():
                    if isinstance(value, gvars['mpl'].axes.Axes):
                        value.grid()

            if self.targs.grid:
                for grid_arg in self.targs.grid:
                    s = grid_arg.split("$")
                    lvargs, lkwargs, rvargs, rkwargs = \
                        parse_subargs(s[0], s[1:], gvars)

                    if rvargs or rkwargs:
                        for ax in lvargs:
                            ax.grid(*rvargs, **rkwargs)
                    elif lvargs or lkwargs:
                        gvars["ax"].grid(*lvargs, **lkwargs)
                    else:
                        gvars["ax"].grid()

            # legend setting
            if self.targs.l:
                for key, value in gvars.items():
                    if isinstance(value, gvars['mpl'].axes.Axes):
                        value.legend()

            if self.targs.legend:
                for legend_arg in self.targs.legend:
                    s = legend_arg.split("$")
                    lvargs, lkwargs, rvargs, rkwargs = \
                        parse_subargs(s[0], s[1:], gvars)

                    if rvargs or rkwargs:
                        for ax in lvargs:
                            ax.legend(*rvargs, **rkwargs)
                    elif lvargs or lkwargs:
                        gvars["ax"].legend(*lvargs, **lkwargs)
                    else:
                        gvars["ax"].legend()


            # execute axes functions
            if self.targs.axes:
                for axes_arg in self.targs.axes:
                    s = axes_arg.split("$")
                    lvargs, lkwargs, rvargs, rkwargs = \
                        parse_subargs(s[0], s[1:], gvars, left_eval=False)

                    if len(lvargs) == 1:
                        ax = "ax"
                        funcname = lvargs[0]
                    elif len(lvargs) == 2:
                        ax = lvargs[0]
                        funcname = lvargs[1]
                    else:
                        UsageError("Following option needs one or two items at the left of @: %s"%yaxis_arg)

                    getattr(gvars[ax], funcname)(*rvargs, **rkwargs)

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
                    lvargs, lkwargs, rvargs, rkwargs = \
                        parse_subargs(s[0], s[1:], gvars)

                    name = lvargs.pop(0)

                    if gvars['num_pages'] > 1:
                        root, ext = os.path.splitext(name)
                        name = '%s-%d%s'%(root, gvars['page_num'], ext)

                    gvars["figure"].savefig(name, *lvargs, **lkwargs)

            if gvars["B"]:
                gvars["B"].savefig(figure=gvars["figure"])

            # displyaing an image on screen
            if not self.targs.noshow:
                gvars['pyplot'].show()

            gvars["figure"].clear()
            gvars["pyplot"].close(gvars["figure"])
            del gvars['figure']
