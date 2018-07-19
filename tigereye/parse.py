# -*- coding: utf-8 -*-
"tigereye task argument parser module."

from .core_tasks import tasks

def _parse(targv):

    # check task name
    handler_cls = tasks.get(targv[0], None)

    # get parser
    if handler_cls:
        return handler_cls(targv[1:])

def teye_task_parse(argv):

    task_argv = []
    for arg in argv:
        if arg == "--":
            if task_argv:
                yield _parse(task_argv)
            task_argv = []
        else:
            task_argv.append(arg)

    if task_argv:
        yield _parse(task_argv)
