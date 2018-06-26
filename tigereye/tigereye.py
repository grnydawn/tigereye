# -*- coding: utf-8 -*-
"""tigereye main module."""
from __future__ import absolute_import

# import tigereye features
from .util import support_message, error_exit, parse_funcargs, teye_eval
from .error import InternalError, UsageError
from .parse import teye_parse
from .load import teye_load
from .var import teye_var
from .plot import teye_plot
from .template import (teye_import_data, teye_import_frontpage,
    teye_import_backpage)

def entry():
    import sys
    return main(sys.argv[1:])

def main(argv):

    try:

        # plotting environment
        attrs = {}

        # import core libraries
        import os
        import csv
        import numpy
        import matplotlib
        if os.environ.get('DISPLAY','') == '':
            matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        attrs['csv'] = csv
        attrs['numpy'] = numpy
        attrs['pyplot'] = plt

        # argument and template processing
        args = teye_parse(argv, attrs)

        # import data
        teye_import_data(args, attrs)

        # data collection
        teye_load(args, attrs)

        # plotting variables
        teye_var(args, attrs)

        # exit if noplot option exists
        if 'return' in attrs:
            return attrs['return']

        # multipage
        if args.book:
            vargs, kwargs = parse_funcargs(args.book, attrs)
            if vargs:
                bookfmt = kwargs.pop('format', 'pdf').lower()
                attrs['_page_save'] = kwargs.pop('page_save', False)
                kwargs = ', '.join(['%s=%s'%(k,v) for k,v in kwargs.items()])
                for target in vargs:
                    if bookfmt == 'pdf':
                        from matplotlib.backends.backend_pdf import PdfPages
                        attrs['_pdf_pages'] =  teye_eval('_p("%s", %s)'%(target, kwargs), attrs, _p=PdfPages)
                    else:
                        raise UsageError('Book format, "%s", is not supported.'%bookfmt)

        # import frontpage
        teye_import_frontpage(args, attrs)

        # plot generation
        teye_plot(args, attrs)

        # import backpage
        teye_import_backpage(args, attrs)

        # multi-page closing
        if '_pdf_pages' in attrs:
            attrs['_pdf_pages'].close()

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
