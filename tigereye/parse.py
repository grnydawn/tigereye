# -*- coding: utf-8 -*-
"tigereye task argument parser module."

import sys
import imp
import shlex
import string

from .core_tasks import tasks
from .util import get_localpath, PY3, error_warn

if PY3:
    import importlib
    __import__ = importlib.__import__

def _read_task(targ, gvars):

    from .entry import parse_global_opts

    if targ.find("@") > 0:
        url, varmap = targ.split("@")
    else:
        url, varmap = targ, None

    if url.find("?") > 0:
        path, target = url.split("?")
        impkey, impvalue = target.split("=")
    else:
        path, impkey, impvalue = url, None, None

    localpath = get_localpath(path)

    with open(localpath, "r") as f:
        cmd = f.read()

    teye_cmd = cmd.replace("\n", " ").replace("\\", "")

    iargs = shlex.split(teye_cmd)

    if iargs and (iargs[0] in tasks.keys() or not iargs[0].startswith("-")):
        iargs.pop(0)

    gargs, task_argv = parse_global_opts(iargs)

    # handling task commands
    imported_task_argv = []
    for tname, targv, task_cls in teye_task_parse(task_argv, gvars):
        task = task_cls(targv)
        if impkey is None or getattr(task.targs, impkey.strip(), False) == impvalue.strip():
            for name, value in task.targs._get_kwargs():
                if value:
                    if isinstance(value, list):
                        for v in value:
                            if len(name) == 1:
                                imported_task_argv.append("-"+name)
                            else:
                                imported_task_argv.append("--"+name)
                            if varmap:
                                imported_task_argv.append(v + "$" + varmap)
                            else:
                                imported_task_argv.append(v)
                    else:
                        if len(name) == 1:
                            imported_task_argv.append("-"+name)
                        else:
                            imported_task_argv.append("--"+name)
                        if varmap:
                            imported_task_argv.append(value + "$" + varmap)
                        else:
                            imported_task_argv.append(value)
    return imported_task_argv

def _read_function(targ, gvars):

    impfuncs = {}

    if targ.find("?") > 0:
        path, target = targ.split("?")
        for pair in target.split("&"):
            impkey, impvalue = pair.split("=")
            if impkey == "name":
                impfuncs[impvalue.strip()] = None
    else:
        path = targ

    localpath = get_localpath(path)

    with open(localpath, "r") as f:
        mod = f.read()


    mymod = imp.new_module('extfunc')
    funcs = {}
    exec(mod, mymod.__dict__, funcs)

    for funcname in impfuncs.keys():
        impfuncs[funcname] = funcs[funcname]

    return impfuncs

def _import(targv, gvars):

    new_targv = []
    imp_funcs = {}
    task_found = False
    function_found = False
    module_found = False

    for targ in targv:

        if task_found:
            new_targv.extend(_read_task(targ, gvars))
            task_found = False
        elif function_found:
            imp_funcs = _read_function(targ, gvars)
            function_found = False
        elif module_found:
            items = targ.split("@")
            mod = __import__(items[0].strip())
            if len(items) == 2:

                if items[1].strip() not in string.ascii_uppercase[:26]:
                    gvars[k] = v
                else:
                    error_warn("'%s' is a reserved word."%k)

                gvars[items[0].strip()] = gvars[items[1].strip()] = mod
            elif len(items) == 1:
                gvars[items[0].strip()] = mod
            module_found = False
        elif targ == "--import-task":
            task_found = True
        elif targ == "--import-function":
            function_found = True
        elif targ == "--import-module":
            module_found = True
        else:
            new_targv.append(targ)

    return new_targv, imp_funcs

def _parse(targv, gvars):
    tname = targv[0]
    new_targv, imp_funcs = _import(targv[1:], gvars)

    for k, v in imp_funcs.items():
        if k not in string.ascii_uppercase[:26]:
            gvars[k] = v
        else:
            error_warn("'%s' is a reserved word."%k)

    tcls = tasks.get(tname, None)

    return tname, new_targv, tcls

def teye_task_parse(argv, gvars):

    task_argv = []
    for arg in argv:
        if arg == "--":
            if task_argv:
                yield _parse(task_argv, gvars)
            task_argv = []
        else:
            task_argv.append(arg)

    if task_argv:
        yield _parse(task_argv, gvars)
