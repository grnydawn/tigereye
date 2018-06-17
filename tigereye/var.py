# -*- coding: utf-8 -*-
"""tigereye data read module."""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import re

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
                    raise Exception('Unknown %s argument format: %s'%(
                        vname, formula))

