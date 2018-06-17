# -*- coding: utf-8 -*-
"""tigereye main module."""
from __future__ import absolute_import

# import tigereye features
from .util import support_message, error_exit
from .error import InternalError, UsageError
from .parse import teye_parse
from .load import teye_load
from .var import teye_var
from .plot import teye_plot

def main(argv):

    try:

        # plotting attributes
        attrs = {}

        # import core libraries
        import numpy
        import matplotlib.pyplot as plt
        attrs['pyplot'] = plt
        attrs['numpy'] = numpy

        # argument and template processing
        args = teye_parse(argv, attrs)

        # data collection
        teye_load(args, attrs)

        # plotting variables
        teye_var(args, attrs)

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
