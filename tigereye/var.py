# -*- coding: utf-8 -*-
"""tigereye data read module."""

from __future__ import (absolute_import, division,
                        print_function)
import sys
import re

from .util import teye_eval, _DEBUG, get_var
from .error import UsageError

_re_did = re.compile(r'(?P<did>d\d+)(?P<others>.*)')

def teye_var(args, attrs):

    if args.variable:
        for var in args.variable:
            vname, formula = get_var(var)
        #for vname, formula in get_var(args.variable):
            if formula[0]=='d':
                match = _re_did.match(formula)
                if match:
                    did = match.group('did')
                    others = match.group('others')
                    if others and others[0] == '.':
                        others = others[1:]
                    attrs[did].get_data(vname, others, attrs)
            elif formula[0:5]=='numpy':
                handler = attrs['_build_handlers']['numpybuild']()
                handler.get_data(vname, formula[6:].strip(), attrs)
            else:
                try:
                    attrs[vname] = teye_eval(formula, attrs)
                except:
                    raise Exception('Unknown %s argument format: %s'%(
                        vname, formula))

    if args.calc:
        for calc in args.calc:
        #for vname, formula in get_var(args.calc):
            vname, formula = get_var(calc)
            attrs[vname] = teye_eval(formula, attrs)

    if args.value:
        for pval in args.value:
            val = teye_eval(pval, attrs)
            print("Value of '%s' = %s"%(pval, str(val)))

    if args.noplot:
        if _DEBUG:
            attrs['return'] = 1
        else:
            attrs['return'] = 0

