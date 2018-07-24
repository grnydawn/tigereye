# -*- coding: utf-8 -*-
"tigereye data load module."

import os
import filetype
import tempfile

from .error import UsageError
from .util import (teval, parse_subargs, funcargs_eval, get_localpath,
    )

def _reader_by_ext(ext, pd):

    if ext in (".csv",):
        return pd.read_csv
    else:
        import pdb; pdb.set_trace()

def _read_data(data_format, idx, target, gvars):

    if data_format:
        # user-specified formats
        for fmt in data_format:
            lvargs, lkwargs, rvargs, rkwargs = \
                parse_subargs(fmt, [], {}, left_eval=False, right_eval=False)
            if rvargs or rkwargs:
                if not lvargs or str(idx) in lvargs:
                    reader = getattr(gvars["pd"], "read_"+rvargs[0].strip())
                    attrs = [k+"="+v for k, v in rkwargs.items()]
                    vargs, kwargs = funcargs_eval(",".join(attrs), [], gvars)
                    return reader(target, **kwargs)
            else:
                reader = getattr(gvars["pd"], "read_"+lvargs[0].strip())
                attrs = [k+"="+v for k, v in lkwargs.items()]
                vargs, kwargs = funcargs_eval(",".join(attrs), [], gvars)
                return reader(target, **kwargs)
    else:
        readers = [getattr(gvars['pd'], v) for v in dir(gvars['pd']) if v.startswith("read_")]
        _,ext = os.path.splitext(target)
        readers.insert(0, _reader_by_ext(ext, gvars['pd']))
        for reader in readers:
            try:
                return reader(target)
            except Exception as err:
                pass

def teye_data_load(gargs, gvars):

    data_objs = []
    gvars['D'] = data_objs

    for idx, item in enumerate(gargs.data):
        local_path = get_localpath(item)
        if local_path:
            data_obj = _read_data(gargs.data_format, idx, local_path, gvars)
            if data_obj is not None:
                data_objs.append(data_obj)
        elif item.startswith("pandas.") or item.startswith("pd."):
            s = item.split("$")
            data_objs.append(teval(s[0], s[1:], gvars))
        elif item.startswith("numpy.") or item.startswith("np."):
            s = item.split("$")
            npdata = teval(s[0], s[1:], gvars)
            dim = len(npdata.shape)
            if dim == 1:
                data_objs.append(gvars["pd"].Series(npdata))
            elif dim == 2:
                data_objs.append(gvars["pd"].DataFrame(npdata))
            elif dim == 3:
                data_objs.append(gvars["pd"].Panel(npdata))
            #elif dim == 4:
            #    data_objs.append(gvars["pd"].Panel4D(npdata))
            else:
                UsageError("data dimension should be between 1 and 4")
        else:
            s = item.split("$")
            data = teval(s[0], s[1:], gvars)
            if isinstance(data, (gvars["pd"].Series, gvars["pd"].DataFrame,
                gvars["pd"].Panel)):
                data_objs.append(data)
            elif isinstance(data, (list, tuple)):
                s = item.split("$")
                npdata = teval("np.asarray(%s)"%s[0], s[1:], gvars)
                dim = len(npdata.shape)
                if dim == 1:
                    data_objs.append(gvars["pd"].Series(npdata))
                elif dim == 2:
                    data_objs.append(gvars["pd"].DataFrame(npdata))
                elif dim == 3:
                    data_objs.append(gvars["pd"].Panel(npdata))
                elif dim == 4:
                    data_objs.append(gvars["pd"].Panel4D(npdata))
                else:
                    UsageError("data dimension should be between 1 and 4")
            elif isinstance(data, dict):
                import pdb; pdb.set_trace()
            else:
                raise UsageError("Unknown input data: %s"%item)


    if len(data_objs) == 0:
        gvars['D'] = None
    elif len(data_objs) == 1:
        gvars['D'] = data_objs[0]
    else:
        gvars['D'] = data_objs
