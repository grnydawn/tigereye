# -*- coding: utf-8 -*-
"tigereye main module."

from topcli import CLI, UsageError

from .matplot import matplot_task
from .printing import print_task
from .verifying import verify_task

def entry():
    import sys
    return main(sys.argv[1:])

def main(argv):

    try:

        app = CLI("tigereye")

        app.add_command("matplot", matplot_task)
        app.add_command("print", print_task)
        app.add_command("verify", verify_task)

        return app.run(argv)

    except UsageError as err:

        # error explanation and suggestions
        error_exit(err)
