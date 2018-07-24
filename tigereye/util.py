# -*- coding: utf-8 -*-
"""tigereye utility module."""

import sys
import os
import string
import tempfile

from .error import UsageError

PY3 = sys.version_info >= (3, 0)

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

_builtins = {
    "max":      max
}

class teye_globals(dict):

    def __init__(self, *vargs, **kwargs):
        super(teye_globals, self).__init__(*vargs, **kwargs)
        self['__builtins__'] = _builtins
        for C in string.ascii_uppercase[:26]:
            self[C] = None

    def __setitem__(self, key, item):
        if key in globals()['__builtins__']:
            raise UsageError("builtin name, '%s', can not be overriden."%key)
        super(teye_globals, self).__setitem__(key, item)


def subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in _subclasses(c)])

def error_exit(exc):
    print("ERROR: %s"%str(exc))
    sys.exit(-1)

def teval(expr, varmaps, g, **kwargs):

    def _parse(**kw_str):
        return kw_str

    try:
        _g = dict(g)

        for vmap in varmaps:
            _g.update(teval('_p(%s)'%vmap, [], _g, _p=_parse))

        return eval(expr, _g, kwargs)
    except NameError as err:
        raise UsageError('EVAL: '+str(err))
    except TypeError as err:
        import pdb; pdb.set_trace()

def funcargs_eval(args_str, varmaps, gvars):

    def _parse(*args, **kw_str):
        return list(args), kw_str

    return teval('_p(%s)'%args_str, varmaps, gvars, _p=_parse)


def parse_subargs(text, varmaps, gvars, left_eval=True, right_eval=True):

    def _unstrmap(text, strmap):

        for k, v in strmap.items():
            text = text.replace(k, v)

        return text

    def _strmap(text):
        strmap = {}

        quote = None
        out = []
        buf = []
        for ch in text:
            if ch=='"' or ch=="'":
                if quote:
                    if quote==ch:
                        strid = "tigereyestrmap%d"%len(strmap)
                        out.append(strid)
                        strmap[strid] = "".join(buf)
                        out.append(quote)

                        buf = []
                        quote = None
                    else:
                        buf.append(ch)
                else:
                    quote = ch
                    out.append(quote)
            elif quote:
                buf.append(ch)
            else:
                out.append(ch)

        return "".join(out), strmap

    def _parse(lv, lk, text):

        newtext, strmap = _strmap(text)

        for item in [i.strip() for i in newtext.split(',')]:
            if '=' in item:
                new, old = [i.strip() for i in item.split('=')]
                lk[new] = _unstrmap(old, strmap)
            else:
                lv.append(_unstrmap(item, strmap))

    tsplit = text.split('@')

    if len(tsplit) == 2:
        left, right = tsplit
    elif len(tsplit) == 1:
        left, right = tsplit[0], None

    if left_eval:
        lvargs, lkwargs = funcargs_eval(left, varmaps, gvars)
    else:
        lvargs = []
        lkwargs = {}
        _parse(lvargs, lkwargs, left)


    rvargs = []
    rkwargs = {}

    if right:
        if right_eval:
            rvargs, rkwargs = funcargs_eval(right, varmaps, gvars)
        else:
            varmaps = _parse(rvargs, rkwargs, right)

    return lvargs, lkwargs, rvargs, rkwargs

def get_localpath(path):

    if os.path.isfile(path):
        return path
    elif urllib_imported and urlparse(path).netloc:
        try:
            f = urlopen(path)
            rdata = f.read()
            f.close()
            t = tempfile.NamedTemporaryFile(delete=False)
            t.write(rdata)
            t.close()
            return t.name
        except HTTPError as e:
            error_exit(e)
        except URLError as e:
            error_exit(e)
