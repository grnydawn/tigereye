# -*- coding: utf-8 -*-
"tigereye main module."

import sys

from .error import InternalError, UsageError, NormalExit
from .util import teye_globals, error_exit
from .entry import teye_entry_task
from .parse import teye_task_parse
from .mgmt import teye_mgmt_task

def entry():
    return main(sys.argv[1:])

def _exit_task(gvars):

    if gvars["B"]:
        gvars["B"].close()

def main(argv):

    if teye_mgmt_task(argv):
        return 0

    try:

        # tigereye global variables
        gvars = teye_globals()

        # handling entry command and global options
        newargv = teye_entry_task(argv, gvars)

        # handling task commands
        for tname, targv, task_cls in teye_task_parse(newargv, gvars):

            if task_cls is not None:
                task_cls(targv).run(gvars)

        _exit_task(gvars)

    except InternalError as err:

        # ask for sending data
        error_exit(err)

    except UsageError as err:

        # error explanation and suggestions
        error_exit(err)

    except ImportError as err:

        # python related suggestion
        error_exit(err)

    except NormalExit as out:
        return 0

    else:
        return 0

