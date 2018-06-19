# -*- coding: utf-8 -*-
"""tigereye utility module."""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import sys

_DEBUG = True

builtins = {
#    'abs': abs,
#    'all': all,
#    'any': any,
#    'ascii': ascii,
#    'bin': bin,
#    'bool': bool,
#    'bytearray': bytearray,
#    'bytes': bytes,
#    'callable': callable,
#    'chr': chr,
#    'complex': complex,
#    'dict': dict,
#    'divmod': divmod,
#    'enumerate': enumerate,
#    'iter': iter,
#    'format': format,
#    'frozenset': frozenset,
#    'getattr': getattr,
#    'hasattr': hasattr,
#    'hash': hash,
#    'hex': hex,
#    'int': int,
#    '': int,
#    '': f,
    'False': False,
    'max': max,
    'min': min,
    'object': object,
    'True': True,
#    '': f,
#    '': f,
}

#        Built-in Functions      
#abs()   dict()  help()  min()   setattr()
#all()   dir()   hex()   next()  slice()
#any()   divmod()    id()    object()    sorted()
#ascii() enumerate() input() oct()   staticmethod()
#bin()   eval()  int()   open()  str()
#bool()  exec()  isinstance()    ord()   sum()
#bytearray() filter()    issubclass()    pow()   super()
#bytes() float() iter()  print() tuple()
#callable()  format()    len()   property()  type()
#chr()   frozenset() list()  range() vars()
#classmethod()   getattr()   locals()    repr()  zip()
#compile()   globals()   map()   reversed()  __import__()
#complex()   hasattr()   max()   round()  
#delattr()   hash()  memoryview()    set()    


# for debugging purpose
_DEBUG_LEVEL = 3 # 0: no debug, 1~3: higher is more debugging information

PY3 = sys.version_info >= (3, 0)

def teye_eval(expr, g={'__builtins__': builtins}, l={}):
    return eval(expr, g, l)

def teye_exec(obj, g={'__builtins__': builtins}, l={}):
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
