# -*- coding: utf-8 -*-
"""tigereye main module."""
from __future__ import absolute_import

import os
import sys
import copy

# import tigereye features
from .util import support_message, error_exit, teye_dict
from .error import InternalError, UsageError, NormalExit
from .parse import teye_parse
from .var import teye_var
from .plot import cmd_plot

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
    return main(sys.argv[1:])

def main(argv):

    try:

        # plotting environment
        attrs = teye_dict()

        # import core libraries
        _import_libs(attrs)

        # argument and template processing
        for cmd, args in teye_parse(argv, attrs):

            cmd(args, attrs)

    except InternalError as err:

        print(err.error_message())
        error_exit(support_message())

    except UsageError as err:
        import pdb; pdb.set_trace()
        print(err.error_message())
        error_exit("UsageError")

    except ImportError as err:

        error_exit(str(err))

    except NormalExit as out:

        error_exit(str(err))

    else:
        return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
