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
    "False":    False,
    "len":      len,
    "max":      max,
    "min":      min,
    "range":    range,
    "True":     True,
}

def args_pop(args, name, num_remove):
    target = []
    newargs = []
    nitems = 0

    for arg in args:
        if nitems > 0:
            target[-1].append(arg)
            nitems -= 1
        elif arg == name:
            target.append([])
            nitems = num_remove
        else:
            newargs.append(arg)

    return newargs, target

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

def error_warn(exc):
    print("WARNING: %s"%str(exc))

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


def parse_optionvalue(text, varmaps, gvars, evals=None):

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

    def _parse(text):

        lv = []
        lk = {}

        newtext, strmap = _strmap(text)

        for item in [i.strip() for i in newtext.split(',')]:
            if '=' in item:
                new, old = [i.strip() for i in item.split('=')]
                lk[new] = _unstrmap(old, strmap)
            else:
                lv.append(_unstrmap(item, strmap))

        return (lv, lk)

    out = []

    tsplit = text.split('@')
    right = tsplit[-1]

    levals = 0 if evals is None else len(evals)
    litems = len(tsplit[:-1])
    assert levals == 0 or litems <= levals

    for idx, left in enumerate(tsplit[:-1]):
        if levals == 0 or idx >= levals or evals[idx+levals-litems] is not True:
            out.append(_parse(left))
        else:
            out.append(funcargs_eval(left, varmaps, gvars))

    vargs, kwargs = funcargs_eval(right, varmaps, gvars)

    return out, vargs, kwargs

def get_localpath(path):

    if os.path.isfile(path):
        return path
    elif urllib_imported and urlparse(path).netloc:
        try:
            f = urlopen(path)
            rdata = f.read()
            f.close()
            _, ext = os.path.splitext(path)
            t = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
            t.write(rdata)
            t.close()
            return t.name
        except HTTPError as e:
            error_exit(e)
        except URLError as e:
            error_exit(e)
