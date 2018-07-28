# -*- coding: utf-8 -*-
"tigereye management task module."

def _first_task_argv(argv):
    taskargv = []

    for arg in argv:
        if arg == "--":
            break
        else:
            taskargv.append(arg)

    return taskargv

def _config_task(argv):
    import pdb; pdb.set_trace()

def _add_task(argv):
    import pdb; pdb.set_trace()

def _remove_task(argv):
    import pdb; pdb.set_trace()

def _register_task(argv):
    import pdb; pdb.set_trace()

def _search_task(argv):
    import pdb; pdb.set_trace()

def teye_mgmt_task(argv):
    if argv:
        if argv[0] == "config":
            _config_task(_first_task_argv(argv[1:]))
        elif argv[0] == "add":
            _add_task(_first_task_argv(argv[1:]))
        elif argv[0] == "remove":
            _remove_task(_first_task_argv(argv[1:]))
        elif argv[0] == "register":
            _register_task(_first_task_argv(argv[1:]))
        elif argv[0] == "search":
            _search_task(_first_task_argv(argv[1:]))
        else:
            return

        return True
    else:
        return
