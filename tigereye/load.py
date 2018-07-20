# -*- coding: utf-8 -*-
"tigereye data load module."

import os
import filetype
import tempfile

from .error import UsageError
from .util import PY3, error_exit, teval, parse_subargs, funcargs_eval

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

class TEyeType(filetype.Type):
    pass

class Csv(TEyeType):
    """
    Implements the CSV data type matcher.
    """
    MIME = 'text/csv'
    EXTENSION = 'csv'
    PANDAS = 'csv'

    def __init__(self):
        super(Csv, self).__init__(
            mime=Csv.MIME,
            extension=Csv.EXTENSION
        )

    def match(self, buf):
        return (len(buf) > 2 and
                buf[0] == 0xFF and
                buf[1] == 0xD8 and
                buf[2] == 0xFF)

def _add_filetypes():
    filetype.add_type(Csv())

def _guessread_data(data_format, idx, target):
        
    import pdb; pdb.set_trace()
    data = None

    kind = filetype.guess(target)
    #for reader in [getattr(gvars['pd'], v) for v in dir(gvars['pd']) if v.startswith("read_")]:
    #    try:
    #        data = reader(target)
    #    except Exception as err:
    #        pass
    #    if data is not None:
    #        break

def _read_data(data_format, idx, target, gvars):

    # user-specified formats
    for fmt in data_format:
        lvargs, lkwargs, rvargs, rkwargs = \
            parse_subargs({}, fmt, left_eval=False, right_eval=False)
        if rvargs or rkwargs:
            if not lvargs or str(idx) in lvargs:
                reader = getattr(gvars["pd"], "read_"+rvargs[0].strip())
                attrs = [k+"="+v for k, v in rkwargs.items()]
                vargs, kwargs = funcargs_eval(gvars, ",".join(attrs))
                return reader(target, **kwargs)
        else:
            reader = getattr(gvars["pd"], "read_"+lvargs[0].strip())
            attrs = [k+"="+v for k, v in lkwargs.items()]
            vargs, kwargs = funcargs_eval(gvars, ",".join(attrs))
            return reader(target, **kwargs)

def teye_data_load(gargs, gvars):

    data_objs = []

    for idx, item in enumerate(gargs.data):
        if os.path.isfile(item):
            data_obj = _read_data(gargs.data_format, idx, item, gvars)
            if data_obj is None:
                data_obj = _guessread_data(item)
            if data_obj is not None:
                data_objs.append(data_obj)

        elif urllib_imported and urlparse(item).netloc:
            try:
                f = urlopen(item)
                if PY3:
                    rdata = f.read().decode('utf-8')
                else:
                    rdata = f.read()
                f.close()
                t = tempfile.NamedTemporaryFile(delete=False)
                t.write(rdata)
                t.close()
                data_obj = _read_data(gargs.data_format, idx, t.name, gvars)
                if data_obj is None:
                    data_obj = _guessread_data(rdata)
                if data_obj is not None:
                    data_objs.append(data_obj)
            except HTTPError as e:
                error_exit(e)
            except URLError as e:
                error_exit(e)
        elif item.startswith("pandas.") or item.startswith("pd."):
            data_objs.append(teval(item, gvars))
        elif item.startswith("numpy.") or item.startswith("np."):
            npdata = teval(item, gvars)
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
        else:
            data = teval(item, gvars)
            if isinstance(data, (list, tuple)):
                npdata = teval("np.asarray(%s)"%item, gvars)
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
                raise UserError("Unknown input data: %s"%item)


    if len(data_objs) == 0:
        gvars['D'] = None
    elif len(data_objs) == 1:
        gvars['D'] = data_objs[0]
    else:
        gvars['D'] = data_objs
