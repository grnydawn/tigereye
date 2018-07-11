# -*- coding: utf-8 -*-
"""tigereye data read module."""

from __future__ import (absolute_import, division,
                        print_function)
import sys
import re
import copy

from .util import _eval, _DEBUG, read_template, import_module, parse_subargs, funcargs_eval
from .error import UsageError
from .parse import teye_parse

_re_did = re.compile(r'(?P<did>d\d+)(?P<others>.*)')

def teye_var(args, attrs):

    # import external function
    if args.import_function:
        for import_function_opt in args.import_function:
            importvars, import_args = [i.strip() for i in import_function_opt.split('=', 1)]
            newattrs = copy.copy(attrs)
            if import_args:
                mod = import_module(_eval(import_args, newattrs))
                if importvars:
                    for vpair in importvars.split(','):
                        vpair = vpair.split(':')
                        if len(vpair) == 1:
                            attrs[vpair[0].strip()] = mod[vpair[0].strip()]
                        elif len(vpair) == 2:
                            attrs[vpair[0].strip()] = mod[vpair[1].strip()]
                        else:
                            raise UsageError('The syntax of import function is not correct: %s'%importvars)
                else:
                    raise UsageError('There is no function to import: %s'%import_function_opt)
            else:
                raise UsageError('The syntax of function import is not correct: %s'%import_args)

    # import external data
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
                            raise UsageError('The syntax of import variable is not correct: %s'%importvars)
                else:
                    raise UsageError('There is no variable to import: %s'%import_data_opt)
            else:
                raise UsageError('There should be only one data template target: %s'%import_args)

    if args.variable:
        for var in args.variable:
            vargs, kwargs = funcargs_eval(attrs, var)
            assert not vargs
            attrs.update(kwargs)
#            vname, formula = get_var(var)
#            if formula[0]=='d':
#                match = _re_did.match(formula)
#                if match:
#                    did = match.group('did')
#                    others = match.group('others')
#                    if others and others[0] == '.':
#                        others = others[1:]
#                    attrs[did].get_data(vname, others, attrs)
#            elif formula[0:5]=='numpy':
#                handler = attrs['_build_handlers']['numpybuild']()
#                handler.get_data(vname, formula[6:].strip(), attrs)
#            else:
#                try:
#                    attrs[vname] = _eval(formula, attrs)
#                except:
#                    raise Exception('Unknown %s argument format: %s'%(
#                        vname, formula))

    if args.calc:
        for calc in args.calc:
            vname, formula = get_var(calc)
            attrs[vname] = _eval(formula, attrs)

    if args.value:
        for pval in args.value:
            val = _eval(pval, attrs)
            print("Value of '%s' = %s"%(pval, str(val)))

    if args.noplot:
        if _DEBUG:
            attrs['return'] = 1
        else:
            attrs['return'] = 0

