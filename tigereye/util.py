# -*- coding: utf-8 -*-
"""tigereye utility module."""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import sys

# for debugging purpose
_DEBUG_LEVEL = 3 # 0: no debug, 1~3: higher is more debugging information

PY3 = sys.version_info >= (3, 0)

def teye_eval(expr, g={}, l={}):
    return eval(expr, g, l)

def teye_exec(obj, g={}, l={}):
    exec(obj, g, l)

def error_exit(msg):
    print("Error: %s"%msg)
    sys.exit(-1)

def support_message():
    return "Please send ..."

def temp_attrs(attrs, add_attrs):
    new_attrs = dict(attrs)
    new_attrs.update(add_attrs)
    return new_attrs
