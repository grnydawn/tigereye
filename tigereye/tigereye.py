# -*- coding: utf-8 -*-
"""tigereye main module."""
from __future__ import absolute_import

import os
import copy

# import tigereye features
from .util import support_message, error_exit, teye_dict
from .error import InternalError, UsageError, NormalExit
from .parse import teye_parse
from .load import teye_load
from .var import teye_var
from .plot import teye_plot, cmd_plot

def _import_libs(attrs):

    import numpy

    if os.environ.get('DISPLAY','') == '':
        import matplotlib
        matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    attrs['numpy'] = numpy
    attrs['pyplot'] = plt

    try:
        import pandas
        attrs['pandas'] = pandas
    except ImportError:
        pass

    try:
        import dask
        attrs['dask'] = dask
    except ImportError:
        pass

def entry():
    import sys
    return main(sys.argv[1:])

def main(argv):

    try:

        # plotting environment
        attrs = teye_dict()

        # import core libraries
        _import_libs(attrs)

        commands = {'plot':(cmd_plot.__doc__.split('\n'), cmd_plot)}

        # argument and template processing
        for args in teye_parse(argv, attrs, commands):

            # data collection
            teye_load(args, attrs)

            # plotting variables
            teye_var(args, attrs)

            cmd_plot(args, attrs)

    except InternalError as err:

        print(err.error_message())
        error_exit(support_message())

    except UsageError as err:

        print(err.error_message())
        error_exit(args.usage())

    except ImportError as err:

        error_exit(str(err))

    except NormalExit as out:

        error_exit(str(err))

    else:
        return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv[1:]))
