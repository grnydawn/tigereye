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
_re_ax_colon = re.compile(r'(?P<name>ax\d*)\s*:\s*(?P<others>.*)')
_re_ax_equal = re.compile(r'(?P<name>ax\d*)\s*=\s*(?P<others>.*)')
_re_name = re.compile(r'(?P<name>\w+)\s*,?\s*(?P<others>.*)')

_builtins = {
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

class teye_dict(dict):

    def __init__(self, *vargs, **kwargs):
        super(teye_dict, self).__init__(*vargs, **kwargs)
        self['__builtins__'] = _builtins

    def __setitem__(self, key, item):
        if key in globals()['__builtins__']:
            raise UsageError("builtin name, '%s', can not be overriden."%key)
        super(teye_dict, self).__setitem__(key, item)

try:
    if PY3:
        from urllib.request import urlopen
        from urllib.parse import urlparse
        from urllib.error import HTTPError, URLError
    else:
        from urllib2 import urlopen, HTTPError, URLError
        from urlparse import urlparse
    urllib_imported = True
except ImportError as e:
    urllib_imported = False


def _eval(expr, g, **kwargs):
    try:
        #g['__builtins__'] = builtins
        return eval(expr, g, kwargs)
    except NameError as err:
        raise UsageError(str(err))
    except TypeError as err:
        import pdb; pdb.set_trace()

def import_module(path):

    data = read_file(path)

    if data:
        l = {}
        exec(''.join(data), _builtins, l)
        return l

def error_exit(msg):
    print("Error: %s"%msg)
    sys.exit(-1)

def support_message():
    return "Please send ..."

def funcargs_eval(ns, args_str):

    def _parse(*args, **kw_str):
        return args, kw_str

    return _eval('_p(%s)'%args_str, ns, _p=_parse)


def parse_subargs(ns, text, left_eval=True, right_eval=True):

    def _parse(lv, lk, text):
        for item in [i.strip() for i in text.split(',')]:
            if '=' in item:
                new, old = [i.strip() for i in item.split('=')]
                lk[new] = old
            else:
                lv.append(item)

    tsplit = text.split('@')
    if len(tsplit) == 2:
        left, right = tsplit
    elif len(tsplit) == 1:
        left, right = tsplit[0], None

    if left_eval:
        lvargs, lkwargs = funcargs_eval(ns, left)
    else:
        lvargs = []
        lkwargs = {}
        _parse(lvargs, lkwargs, left)

    if right_eval:
        rvargs, rkwargs = funcargs_eval(ns, right)
    else:
        rvargs = []
        rkwargs = {}
        _parse(rvargs, rkwargs, left)

    return lvargs, lkwargs, rvargs, rkwargs

#
#def parse_funcargs(args_str, attrs):
#
#    def _parse(*args, **kw_str):
#        return args, kw_str
#
#    return _eval('_p(%s)'%args_str, attrs, _p=_parse)
#

def args_pop(args, name, num_remove):
    if name in args:
        for idx in [args.index(name)]*(num_remove+1):
            del args[idx]

def _parse_item(text, recompile):

    match = recompile.match(text)
    if match:
        return match.group('name'), match.group('others')
    else:
        raise UsageError('The syntax of data definition is not correct: %s'%text)

#def get_var(var):
#
#    return _parse_item(var, _re_var)
#
#def get_did(did):
#
#    return _parse_item(var, _re_did)
#
def get_axis(arg, delimiter=':'):

    if delimiter == ':':
        pattern = _re_ax_colon
    elif delimiter == '=':
        pattern = _re_ax_equal
    else:
        raise UsageError('Unknown delimiter during axis parsing:: %s, %s'%(args, delimiter))

    try:
        return _parse_item(arg, pattern)
    except UsageError as err:
        return 'ax', arg

def get_name(arg):

    try:
        return _parse_item(arg, _re_name)
    except UsageError as err:
        return arg, ''

def read_file(path):

    data = None

    if os.path.isfile(path):
        with open(path, mode="r") as f:
            data = f.readlines()

    elif urllib_imported:
        try:
            if urlparse(path).netloc:
                f = urlopen(path)
                if PY3:
                    data = f.read().decode('utf-8')
                    data = data.split('\n')
                else:
                    data = f.readlines()
                f.close()
        except HTTPError as e:
            error_exit("HTTP Error: %s %s"%(str(e.code), template))
        except URLError as e:
            error_exit("URL Error: %s %s"%(str(e.reason), template))
    else:
        error_exit("Input template syntax error: '%s'"%template)

    return data

def read_template(template):

    data = read_file(template)

    if data:
        lines = []
        for line in data:
            line = line.strip()
            if line and line[-1] == '\\':
                line = line[:-1]
            lines.append(line)
        return shlex.split(' '.join(lines))
