# -*- coding: utf-8 -*-
"topcli builtin task module."

from .task import Task

class config_task(Task):

    def __init__(self, targv):

#        self.parser.add_argument('-f', metavar='figure creation', help='define a figure for plotting.')
#        self.parser.add_argument('-t', '--title', metavar='title', action='append', help='title  plotting.')
#        self.parser.add_argument('-p', '--plot', metavar='plot type', action='append', help='plot type for plotting.')
#        self.parser.add_argument('-s', '--save', metavar='save', action='append', help='file path to save png image.')
#        self.parser.add_argument('-x', '--xaxis', metavar='xaxis', action='append', help='axes function wrapper for x axis settings.')
#        self.parser.add_argument('-y', '--yaxis', metavar='yaxis', action='append', help='axes function wrapper for y axis settings.')
#        self.parser.add_argument('-z', '--zaxis', metavar='zaxis', action='append', help='axes function wrapper for z axis settings.')
#        self.parser.add_argument('-g', action='store_true', help='grid for ax plotting.')
#        self.parser.add_argument('-l', action='store_true', help='legend for ax plotting')
#        self.parser.add_argument('--pandas', metavar='pandas', action='append', help='pandas plots.')
#        self.parser.add_argument('--pages', metavar='pages', help='page settings.')
#        self.parser.add_argument('--page-calc', metavar='page_calc', action='append', help='python code for manipulating data within page generation.')
#        self.parser.add_argument('--legend', metavar='legend', action='append', help='plot legend')
#        self.parser.add_argument('--grid', metavar='grid', action='append', help='grid for plotting.')
#        self.parser.add_argument('--subplot', metavar='subplot', action='append', help='define subplot.')
#        self.parser.add_argument('--figure', metavar='figure function', action='append', help='define Figure function.')
#        self.parser.add_argument('--axes', metavar='axes', action='append', help='define Axes function.')
#        self.parser.add_argument('--noshow', action='store_true', default=False, help='prevent showing plot on screen.')
#        self.parser.add_argument('--noplot', action='store_true', default=False, help='prevent generating plot.')
        self.parser.add_argument('--version', action='version', version='tigereye plotting task version 0.0.0')

        self.targs = self.parser.parse_args(targv)

    def perform(self, gvars):

        import pdb; pdb.set_trace()

builtin_tasks = {
    "config": config_task,
}

#    if argv:
#        if argv[0] == "config":
#            _config_task(_first_task_argv(argv[1:]))
#        elif argv[0] == "add":
#            _add_task(_first_task_argv(argv[1:]))
#        elif argv[0] == "remove":
#            _remove_task(_first_task_argv(argv[1:]))
#        elif argv[0] == "register":
#            _register_task(_first_task_argv(argv[1:]))
#        elif argv[0] == "search":
#            _search_task(_first_task_argv(argv[1:]))
#        else:
#            return
#
#        return True
#    else:
#        return
