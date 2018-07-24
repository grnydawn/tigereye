# -*- coding: utf-8 -*-
"tigereye task argument parser module."

import shlex

from .core_tasks import tasks
from .util import get_localpath

def _read_task(targ):

    from .entry import parse_global_opts

    # add $ D=D to argument
    # TODO: support without @ and ?
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
    for tname, targv, task_cls in teye_task_parse(task_argv):
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

def _import(targv):

    new_targv = []
    imp_argv = []
    found = False

    for targ in targv:

        if found:
            new_targv.extend(_read_task(targ))
            found = False
        elif targ in ("-i", "--import"):
            found = True
        else:
            new_targv.append(targ)

    return new_targv

def _parse(targv):
    return targv[0], _import(targv[1:]), tasks.get(targv[0], None)

def teye_task_parse(argv):

    task_argv = []
    for arg in argv:
        if arg == "->":
            if task_argv:
                yield _parse(task_argv)
            task_argv = []
        else:
            task_argv.append(arg)

    if task_argv:
        yield _parse(task_argv)
