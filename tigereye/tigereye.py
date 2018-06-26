# -*- coding: utf-8 -*-
"""tigereye main module."""
from __future__ import absolute_import

import copy

# import tigereye features
from .util import support_message, error_exit, parse_funcargs, teye_eval
from .error import InternalError, UsageError
from .parse import teye_parse
from .load import teye_load
from .var import teye_var
from .plot import teye_plot

def entry():
    import sys
    return main(sys.argv[1:])

def main(argv):

    try:

        # plotting environment
        attrs = {}

        # import core libraries
        import os
        import numpy
        import matplotlib.pyplot as plt
        if os.environ.get('DISPLAY','') == '':
            import matplotlib
            matplotlib.use('Agg')

        attrs['numpy'] = numpy
        attrs['pyplot'] = plt

        # argument and template processing
        #argv = [item.decode("utf-8") for item in argv]
        args = teye_parse(argv, attrs)

        # data collection
        teye_load(args, attrs)

        # plotting variables
        teye_var(args, attrs)

        # exit if noplot option exists
        if 'return' in attrs:
            return attrs['return']

        # plot generation
        teye_plot(args, attrs)

    except InternalError as err:

        print(err.error_message())
        error_exit(support_message())

    except UsageError as err:

        print(err.error_message())
        error_exit(args.usage())

    except ImportError as err:

        error_exit(str(err))

    else:
        return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv[1:]))
