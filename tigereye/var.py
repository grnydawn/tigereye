# -*- coding: utf-8 -*-
"""tigereye data read module."""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import sys
import re

from .util import teye_eval, _DEBUG
from .error import UsageError

_re_did = re.compile(r'(?P<did>d\d+)(?P<others>.*)')
_re_var = re.compile(r'(?P<name>\w+)\s*=\s*(?P<others>.*)')

def _get_var(var):

    for arg in var:
        match = _re_var.match(arg)
        if match:
            yield match.group('name'), match.group('others')
        else:
            raise UsageError('The syntax of data definitiion is not correct: %s'%arg)



def teye_var(args, attrs):

    if args.variable:
        for vname, formula in _get_var(args.variable):
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
        for vname, formula in _get_var(args.calc):
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

