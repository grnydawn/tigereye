# -*- coding: utf-8 -*-
"tigereye data load module."

import os
import tempfile

from .error import UsageError
from .util import (teval, parse_optionvalue, funcargs_eval, get_localpath,
    )

def _reader_by_ext(ext, pd):

    if ext in (".csv",):
        return pd.read_csv
    else:
        import pdb; pdb.set_trace()

def _read_data(data_format, idx, target, gvars):

    if data_format:

        # user-specified formats
        for fmt_arg in data_format:
            # syntax: [input index@]fmtname@funcargs
            s = fmt_arg.split("$")
            items, vargs, kwargs = parse_optionvalue(s[0], s[1:], gvars, evals=[True, False])

            if len(items) == 1:
                fmt = items[0][0][0]
            elif len(items) == 2:
                if idx in items[0][0]:
                    fmt = items[1][0][0]
                else:
                    fmt = None
            else:
                UsageError("The synaxt error near '@': %s"%fmt_arg)

            if fmt:
                reader = getattr(gvars["pd"], "read_"+fmt.strip())
                return reader(target, *vargs, **kwargs)
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
                npdata = teval("np.asarray(%s)"%s[0], s[1:], gvars)
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
            elif isinstance(data, dict):
                import pdb; pdb.set_trace()
            else:
                raise UsageError("Unknown input data: %s"%item)


    if len(data_objs) == 0:
        gvars['D'] = None
    elif len(data_objs) == 1:
        # TODO: in case of stream type, yield multiple times
        gvars['D'] = data_objs[0]
    else:
        gvars['D'] = data_objs
