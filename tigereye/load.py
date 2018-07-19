# -*- coding: utf-8 -*-
"tigereye data load module."

import os
import filetype

from .util import PY3, error_exit, teval, parse_subargs

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
        poscomma = fmt.find(",")
        if poscomma:
            lvargs, lkwargs, rvargs, rkwargs = \
                parse_subargs({}, fmt[poscomma+1:])
            if not rvargs or idx in rvargs:
                reader = getattr(gvars["pd"], "read_"+fmt[:poscomma].strip())
                return reader(target, **lkwargs)
        else:
            raise UsageError("Wrong data format option: %s"%fmt)

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
                data_obj = _read_data(gargs.data_format, idx, rdata, gvars)
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
            pass
            # from numpy to pandas
            #npdata = teval(item, gvars))
            # convert to pandas data
            #data_objs.append(pddata)
            # pandas.Series(data=None, index=None, dtype=None, name=None, copy=False, fastpath=False)
            # pandas.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)
            # pandas.Panel(data=None, items=None, major_axis=None, minor_axis=None, copy=False, dtype=None)
            # pandas.Panel4D(data=None, labels=None, items=None, major_axis=None, minor_axis=None, copy=False, dtype=None)
            
        else:
            # from python data to numpy => asarray
            # from numpy to pandas
            data = teval(item, gvars)
            if isinstance(data) in (list, tuple):
                npdata = teval("np.asarray(%s)"%item, gvars)
                dim = len(npdata.shape)
                import pdb; pdb.set_trace()
            elif isinstance(data) == dict:
                import pdb; pdb.set_trace()
            else:
                raise UserError("Unknown input data: %s"%item)


    gvars['D'] = data_objs
