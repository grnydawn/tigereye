# -*- coding: utf-8 -*-
"topcli cli module."

import importlib



from .error import InternalError, NormalExit
from .name import env_vars
from .entry import entry_task
from .parse import task_parse
from .task import Task
from .config import config
from .builtin import builtin_tasks

class CLI(object):

    def __init__(self, appname, description=None):
        # configure command line interface for appname

        self.name = appname
        self.description = description

        env_vars["A"][self.name] = {}

        self.app_options = []

        self.tasks = dict(builtin_tasks)
        for cmd_name, task_path in config['installed_tasks'].items():
            task = locate_task(task_path)
            self.add_command(cmd_name, task)

        self.default_command = None

        self.exit_tasks = []

        self.modules = {}

    def add_argument(self, handler, *vargs, **kwargs):

        self.app_options.append( (handler, vargs, kwargs) )

    def add_command(self, cmd_name, cmd_task):

        self.tasks[cmd_name] = cmd_task

    def set_default_command(self, cmd_name):

        self.default_command = cmd_name

    def import_module(self, mod_name, alias=None, onfailure=None):

        self.modules[mod_name] = (alias, onfailure)

    def add_exit_task(self, exit_task):

        self.exit_tasks.append(exit_task)

    def run(self, argv):

        try:

            for mod_name, (alias, onfailure) in self.modules.items():
                mod = importlib.import_module(mod_name)
                env_vars["A"][self.name][mod_name.split(".")[-1]] = mod
                if alias:
                    env_vars["A"][self.name][alias] = mod

            # handling entry command and global options
            newargv = entry_task(argv, self.app_options, env_vars["A"][self.name],
                self.tasks, self.default_command, self.description)

            # handling task commands
            for tname, targv, task_cls in task_parse(newargv, env_vars["A"][self.name], self.tasks):

                if task_cls is not None:
                    task_cls(targv).run(gvars)

            for task in self.exit_tasks:
                task(gvars)

        except InternalError as err:

            import pdb; pdb.set_trace()

        except NormalExit as out:

            if out.msg:
                print(out.msg)

            return out.retcode

        except ImportError as err:

            if onfailure:
                onfailure()

        except:

            import sys
            exc_info = sys.exc_info()
            raise exc_info[0], exc_info[1], exc_info[2]

        return 0
