# -*- coding: utf-8 -*-
"tigereye plot core task module."

import argparse

from ..task import Task
from ..util import funcargs_eval, get_axis

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

        self.targs = parser.parse_args(targv)

    def perform(self, gvars):

        gvars['pyplot'] = gvars['plt'] = gvars['mpl'].pyplot

        # pages setting
        if self.targs.pages:
            vargs, kwargs = funcargs_eval(args.pages, gvars)

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
                    vargs, kwargs = funcargs_eval(page_calc, gvars)
                    gvars.update(kwargs)

            # figure setting
            if args.f:
                gvars['figure'] = teval('pyplot.figure(%s)'%args.f, gvars)
            else:
                gvars['figure'] = gvars['pyplot'].figure()

            # plot axis
            if self.targs.ax:
                for ax_arg in self.targs.ax:
                    axname, others = get_axis(ax_arg, delimiter='=')
                    if axname:
                        vargs, kwargs = funcargs_eval(attrs, others)
                        if 'projection' in kwargs and kwargs['projection'] == '3d':
                             from mpl_toolkits.mplot3d import Axes3D
                             attrs['Axes3D'] = Axes3D
                        if len(vargs) == 0 or not isinstance(vargs[0], int):
                            attrs[axname] = _eval('figure.add_subplot(111, %s)'%others, attrs)
                        else:
                            attrs[axname] = _eval('figure.add_subplot(%s)'%others, attrs)
                    else:
                        raise UsageError('Wrong axis option: %s'%ax_arg)
            elif not args.import_plot:
                attrs['ax'] = attrs['figure'].add_subplot(111)


        import pdb; pdb.set_trace()

        # figure


        # multi-pages
