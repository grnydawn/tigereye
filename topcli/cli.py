# -*- coding: utf-8 -*-
"topcli cli module."


from .error import InternalError, NormalExit
from .name import Globals
from .entry import entry_task
from .task import Task
from .config import config

class CLI(object):

    def __init__(self, appname):
        # configure command line interface for appname

        self.name = appname
        self.tasks = dict(config['installed_tasks'])

    def add_command(self, cmdname, cmd_task):
        # add commad statically
        # user can add command using add-task subcommand later

        self.tasks[cmdname] = cmd_task

    def run(self, argv):

        try:

            # tigereye global variables
            gvars = Globals()

            # handling entry command and global options
            newargv = entry_task(argv, gvars)

            # handling task commands
            for tname, targv, task_cls in teye_task_parse(newargv, gvars):

                if task_cls is not None:
                    task_cls(targv).run(gvars)

            _exit_task(gvars)

        except InternalError as err:

            import pdb; pdb.set_trace()

        except NormalExit as out:

            if out.msg:
                print(out.msg)

            return out.retcode

        except:

            import sys
            exc_info = sys.exc_info()
            raise exc_info[0], exc_info[1], exc_info[2]

        return 0
