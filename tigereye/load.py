# -*- coding: utf-8 -*-
"""tigereye data read module."""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os
import shlex
import abc

from .error import UsageError
from .util import PY3, temp_attrs, teye_eval, teye_exec, error_exit

# numpyarray

# csv

# numpytext

# panda
# -read_csv
# -read_json
# -read_html
# -read_clipboard
# -read_excel
# -read_hdf
# -read_feather
# -read_parquet
# -read_msgpack
# -read_stata
# -read_sas
# -read_pickle
# -read_sql
# -read_gbq

# netcdf

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

def _subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in _subclasses(c)])

class Data(object):

    __metaclass__ = abc.ABCMeta

    def __getitem__(self, key):
        return self.data[key]

    @abc.abstractmethod
    def _lib_item(self, vname, cmd, attrs):
        pass

    @abc.abstractmethod
    def _lib_func(self, vname, cmd, params, attrs):
        pass

    def get_data(self, vname, arg, attrs):

        data = self.data
        if vname:
            attrs[vname] = data

        while arg:
            cmd, params, arg = self._parse_arg(arg)
            if cmd[0] == '[' and cmd[-1] == ']':
                data = self._lib_item(vname, cmd, attrs)
            else:
                data = self._lib_func(vname, cmd, params, attrs)
            if self.data is None:
                self.data = data
            if vname:
                attrs[vname] = data

        return data

    def _parse_arg(self, arg):

        cmd = []
        params = []
        others = []

        stack = []
        remained = False

        arg = arg.replace(' ', '__WS__')

        for item in shlex.shlex(arg):

            if remained:
                others.append(item)
                continue

            if stack:
                if item == '(':
                    if stack:
                        params.append(item)
                    stack.append(item)
                elif item == ')':
                    stack.pop()
                    if stack:
                        params.append(item)
                    else:
                        remained = True
                else:
                    params.append(item)
            else:
                if item == '(':
                    stack.append(item)
                elif item == '.':
                    remained = True
                elif item == ')':
                    raise UsageError('Wrong data input syntax: %s'%arg)
                else:
                    cmd.append(item)

        if others and others[0] == ".":
            others = others[1:]

        return (''.join(cmd).replace('__WS__', ' '),
            ''.join(params).replace('__WS__', ' '),
            ''.join(others).replace('__WS__', ' '))

# handler types

class FileData(Data):
    pass
    #def _normalize_filepath(self, path):
    #    if path or path[0] not in ('"', "'") or path[0] != path[-1]:
    #        path = "'%s'"%path
    #    return path

class ValueData(Data):
    pass


# mixins

class BuildMixin(object):

    def __init__(self):
        self.data = None

class NumpyMixin(object):

    def _lib_item(self, vname, cmd, attrs):
        return teye_eval(vname+cmd, l=attrs)

    def _lib_func(self, vname, cmd, params, attrs):
        func = attrs['numpy']
        for name in cmd.split('~'):
            func = getattr(func, name)
        newattrs = temp_attrs(attrs, [('_f_', func)])
        output = teye_eval('_f_(%s)'%params, l=newattrs)
        if output is not None:
            return output
        else:
            return newattrs[vname]


# numpy handlers

class NumpyArrayData(NumpyMixin, ValueData):

    name = 'numpyarray'

    def __init__(self, datasrc, args, attrs):
        if args:
            self.data = teye_eval('numpy.asarray(%s, %s)'%(datasrc, args), l=attrs)
        else:
            self.data = teye_eval('numpy.asarray(%s)'%datasrc, l=attrs)

class NumpyBuildData(NumpyMixin, BuildMixin, ValueData):

    name = 'numpybuild'


class NumpyTextData(NumpyMixin, FileData):

    name = 'numpytext'

    def __init__(self, datasrc, args, attrs):

        if os.path.isfile(datasrc):
            kwargs = ''
            if args:
                kwargs = ', %s'%args
            self.data = teye_eval("numpy.genfromtxt('%s'%s)"%(datasrc, kwargs), l=attrs)
        else:
            error_exit("Input argument syntax error: '%s, %s'"%(datasrc, args))

class CsvTextData(NumpyMixin, FileData):

    name = 'csv'

    def __init__(self, datasrc, args, attrs):

        if os.path.isfile(datasrc):
            kwargs = ', dtype=object'
            if args:
                kwargs += ', %s'%args
            self.data = teye_eval("numpy.genfromtxt('%s'%s)"%(datasrc, kwargs), l=attrs)
        else:
            error_exit("Input argument syntax error: '%s, %s'"%(datasrc, args))

# handler groups
_file_format_handlers = list(
    cls for cls in _subclasses(FileData) if hasattr(cls, 'name'))
_value_format_handlers = list(
    cls for cls in _subclasses(ValueData) if hasattr(cls, 'name'))
_build_handlers = dict(
    (cls.name, cls) for cls in _subclasses(BuildMixin) if hasattr(cls, 'name'))
_data_handlers = dict(
    (cls.name, cls) for cls in _subclasses(Data) if hasattr(cls, 'name'))

def _select_srcfmt(datasrc, attrs):
    if os.path.isfile(datasrc):
        for cls in _file_format_handlers:
            try:
                return cls(datasrc, None, attrs)
            except:
                pass
    else:
        for cls in _value_format_handlers:
            try:
                return cls(datasrc, None, attrs)
            except:
                pass

    if urllib_imported:
        pass
        #import pdb; pdb.set_trace()

def teye_load(args, attrs):

    _data_objects = []

    # read data files
    srcfmts = [None for _ in range(len(args.data_sources))]
    global_fmt = None

    # format: 0:name, ... or name, ...
    if args.data_format:
        for fmt in args.data_format:
            try:
                comma = fmt.find(',')
                colon = fmt.find(':')
                if comma > 0 and colon > 0:
                    if comma > colon:
                        handler_name = fmt[comma+1:colon].replace(' ', '')
                        handler = _data_handlers[handler_name]
                        srcfmts[int(fmt[:comma])] = (handler, fmt[colon+1:])
                    else:
                        print('Warning: source format syntax error (ignored): %s'%fmt)
                elif comma > 0:
                    handler_name = fmt[:comma].replace(' ', '')
                    global_fmt = (_data_handlers[handler_name], fmt[comma+1:])
                else:
                    global_fmt = (_data_handlers[fmt], None)

            except:
                print('Warning: source format syntax error (ignored): %s'%fmt)

    if global_fmt is not None:
        for idx in range(len(args.data_sources)):
            if srcfmts[idx] is None:
                srcfmts[idx] = global_fmt

    for idx, data_source in enumerate(args.data_sources):

        if srcfmts[idx] is None:
            data = _select_srcfmt(data_source, attrs)
        else:
            data = srcfmts[idx][0](data_source, srcfmts[idx][1], attrs)

        if data:
            attrs['d%d'%idx] = data
            _data_objects.append(data)
        else:
            raise UsageError('"%s" is not loaded correctly.'%data_source)

    attrs['_data_objects'] = _data_objects
    attrs['_build_handlers'] = _build_handlers
