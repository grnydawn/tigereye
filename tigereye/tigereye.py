# -*- coding: utf-8 -*-
"tigereye main module."

import sys

from topcli import CLI, UsageError

from .matplot import matplot_task
from .printing import print_task
from .verifying import verify_task

def entry():
    return main(sys.argv[1:])

def main(argv):

    def _matplotlib_import_error():
        print("ERROR: can not import 'matplotlib' module.")
        sys.exit(-1)

    def _pdf_bind_handler(headers, vargs, kwargs):

        from matplotlib.backends.backend_pdf import PdfPages
        return { "pdf_pages": PdfPages(*vargs, **kwargs) }

    try:

        app = CLI("tigereye", description="reusable plotting command")

        app.add_argument(_pdf_bind_handler, "--pdf-bind", help='generate pdf binding.')
        app.add_argument(None, "--version", action='version', version='tigereye version 0.3.0')

        app.add_command("matplot", matplot_task)
        app.add_command("print", print_task)
        app.add_command("verify", verify_task)

        app.set_default_command("matplot")

        app.import_module("matplotlib", alias="mpl", onfailure=_matplotlib_import_error)
        app.import_module("matplotlib.pyplot", alias="plt", onfailure=_matplotlib_import_error)
        app.import_module("numpy", alias="np", onfailure=None)
        app.import_module("pandas", alias="pd", onfailure=None)

        return app.run(argv)

    except UsageError as err:

        # error explanation and suggestions
        print(err)
        sys.exit(-1)
