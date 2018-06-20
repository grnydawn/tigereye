# -*- coding: utf-8 -*-
"""tigereye data read module."""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import sys
import re

from .util import teye_eval, teye_exec, _DEBUG

_re_did = re.compile(r'(?P<did>d\d+)(?P<others>.*)')

def teye_var(args, attrs):

    # collect values

    maxinputs = max(args.num_xinputs, args.num_yinputs, args.num_zinputs)

    for idx in range(1, maxinputs+1):

        for v in ('x', 'y', 'z'):
            vname = v+str(idx) if idx > 1 else v

            if vname in args and args[vname]:
                formula = args[vname]
                if formula[0]=='d':
                    match = _re_did.match(formula)
                    if match:
                        did = match.group('did')
                        others = match.group('others')
                        attrs[did].get_data(vname, others, attrs)
                elif formula[0:5]=='numpy':
                    handler = attrs['_build_handlers']['numpybuild']()
                    handler.get_data(vname, formula[6:].strip(), attrs)
                else:
                    try:
                        attrs[vname] = teye_eval(formula, l=attrs)
                    except:
                        raise Exception('Unknown %s argument format: %s'%(
                            vname, formula))

    if args.calc:
        for calc in args.calc:
            teye_exec(calc, l=attrs)

    if args.value:
        for pval in args.value:
            val = teye_eval(pval, l=attrs)
            print("Value of '%s' = %s"%(pval, str(val)))

    if args.noplot:
        if _DEBUG:
            attrs['return'] = 1
        else:
            attrs['return'] = 0

