# -*- coding: utf-8 -*-
"tigereye plot core task module."

import argparse

from ..task import Task

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
        import pdb; pdb.set_trace()

        # pdf pages


        # figure


        # multi-pages
