# -*- coding: utf-8 -*-
"""tigereye data and plot importing module."""

from __future__ import (absolute_import, division,
                        print_function)

import copy

from .error import UsageError
from .util import parse_funcargs, read_template
from .parse import teye_parse
from .var import teye_var

def teye_import_data(args, attrs):
    if args.import_data:
        for import_data_opt in args.import_data:
            importvars, import_args = [i.strip() for i in import_data_opt.split('=', 1)]
            newattrs = copy.copy(attrs)
            templates, kwargs = parse_funcargs(import_args, newattrs)
            if len(templates) == 1:
                opts = read_template(templates[0])
                newargs = teye_parse(opts, newattrs)
                newattrs.update(kwargs)
                teye_var(newargs, newattrs)
                if importvars:
                    for vpair in importvars.split(','):
                        vpair = vpair.split(':')
                        if len(vpair) == 1:
                            attrs[vpair[0].strip()] = newattrs[vpair[0].strip()]
                        elif len(vpair) == 2:
                            attrs[vpair[0].strip()] = newattrs[vpair[1].strip()]
                        else:
                            raise UsageError('The syntax of import variable is not correct'%importvars)
                else:
                    raise UsageError('There is no variable to import'%import_data_opt)
            else:
                raise UsageError('There should be only one data template target: %s'%import_args)

def teye_import_plot(args, attrs):

    # add_subplot for the imported plot
    # --import-plot "axlocal: 321, http://dfsd.sdfs.fsd.sf.df.sdf, axremote, local1=remote1,local2=remote2, ..."
    if args.import_plot:
        import pdb; pdb.set_trace()

def teye_import_frontpage(args, attrs):
    if args.front_page:
        import pdb; pdb.set_trace()

def teye_import_backpage(args, attrs):
    if args.back_page:
        import pdb; pdb.set_trace()
