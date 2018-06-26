# -*- coding: utf-8 -*-
"""tigereye utility module."""
from __future__ import (absolute_import, division,
                        print_function)

import sys
import os
import re
import shlex
import io
from .error import UsageError

_DEBUG = True

_re_var = re.compile(r'(?P<name>\w+)\s*=\s*(?P<others>.*)')
_re_did = re.compile(r'(?P<name>d\d+)(?P<others>.*)')

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
    'tuple': tuple,
    'float': float,
    'str': str,
    'len': len,
    'range': range,
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

try:
    if PY3:
        from urllib.request import urlopen
        from urllib.parse import urlparse
    else:
        from urllib2 import urlopen
        from urlparse import urlparse
    urllib_imported = True
except ImportError as e:
    urllib_imported = False


def teye_eval(expr, g, **kwargs):
    try:
        g['__builtins__'] = builtins
        return eval(expr, g, kwargs)
    except NameError as err:
        raise UsageError(str(err))

def error_exit(msg):
    print("Error: %s"%msg)
    sys.exit(-1)

def support_message():
    return "Please send ..."

def parse_funcargs(args_str, attrs):

    def _parse(*args, **kw_str):
        return args, kw_str

    return teye_eval(b'_p(%s)'%args_str, attrs, _p=_parse)


def _parse_name(text, recompile):

    for arg in text:
        match = recompile.match(arg)
        if match:
            yield match.group('name'), match.group('others')
        else:
            raise UsageError('The syntax of data definition is not correct: %s'%arg)

def get_var(var):

    return _parse_name(var, _re_var)

def get_did(did):

    return _parse_name(var, _re_did)

def read_template(template):

    data = None

    if os.path.isfile(template):
        with open(template, mode="r") as f:
            data = f.readlines()

    elif urllib_imported:
        try:
            if urlparse(template).netloc:
                f = urlopen(template)
                data = f.readlines()
                f.close()
        except HTTPError as e:
            error_exit("HTTP Error: %s %s"%(str(e.code), template))
        except URLError as e:
            error_exit("URL Error: %s %s"%(str(e.reason), template))
    else:
        error_exit("Input template syntax error: '%s'"%template)

    if data:
        lines = []
        for line in data:
            line = line.strip()
            if line and line[-1] == '\\':
                line = line[:-1]
            lines.append(line)
        return shlex.split(' '.join(lines))
