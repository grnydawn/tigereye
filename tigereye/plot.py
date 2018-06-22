# -*- coding: utf-8 -*-
"""tigereye plotting module."""

from __future__ import (absolute_import, division,
    print_function, unicode_literals)

import re

from .error import UsageError
from .util import (error_exit, teye_eval, teye_exec, temp_attrs,
    parse_kwargs)

_re_ax_colon = re.compile(r'(?P<ax>ax\d*)\s*:\s*(?P<others>.*)')
_re_ax_equal = re.compile(r'(?P<ax>ax\d*)\s*=\s*(?P<others>.*)')
_re_name = re.compile(r'(?P<name>\w+)\s*,?\s*(?P<others>.*)')

def _get_axis(arg, delimiter=':'):
    match = None
    if delimiter == ':':
        match = _re_ax_colon.match(arg)
    elif delimiter == '=':
        match = _re_ax_equal.match(arg)
    if match:
        return match.group('ax'), match.group('others')
    else:
        return 'ax', arg

def _get_name(arg):

    match = _re_name.match(arg)
    if match:
        return match.group('name'), match.group('others')
    else:
        return '', arg

def gen_plot(args, attrs):

    # plotting
    plots = []
    if args.plot:
        for plot in args.plot:

            ax, plotarg = _get_axis(plot)

            poscomma = plotarg.find(',')
            if poscomma<0:
                raise UsageError('Wrong plot option: %s'%plotarg)
            else:
                pname = plotarg[:poscomma]
                pargs = plotarg[poscomma+1:]
                plot_handle = teye_eval('%s.%s(%s)'%(ax, pname, pargs), l=attrs)

                try:
                    for p in plot_handle:
                        plots.append(p)
                except TypeError:
                    plots.append(plot_handle)

                if pname == 'pie':
                    attrs[ax].axis('equal')

    attrs['plots'] = plots

def axes_main_functions(args, attrs):

    #import inspect

    # title setting
    for title_arg in args.title:
        ax, arg = _get_axis(title_arg)
        title = arg.format(**attrs)
        teye_eval('%s.set_title(%s)'%(ax, title), l=attrs)


    for xaxis_arg in args.xaxis:
        ax, arg = _get_axis(xaxis_arg)
        xaxis = arg.format(**attrs)

        set_xfuncs =  dict((x, getattr(attrs[ax], x)) for x in dir(attrs[ax]) if x.startswith('set_x'))
        parsed_args = parse_kwargs({}, xaxis, attrs)

        for name, func in set_xfuncs.items():
            funckey = name[5:]
            if name[5:] in parsed_args:
                func_args = dict(parsed_args)
                value = func_args.pop(name[5:])
                func(value, **func_args)

    for yaxis_arg in args.yaxis:
        ax, arg = _get_axis(yaxis_arg)
        yaxis = arg.format(**attrs)

        set_yfuncs =  dict((y, getattr(attrs[ax], y)) for y in dir(attrs[ax]) if y.startswith('set_y'))
        parsed_args = parse_kwargs({}, yaxis, attrs)

        for name, func in set_yfuncs.items():
            funckey = name[5:]
            if name[5:] in parsed_args:
                func_args = dict(parsed_args)
                value = func_args.pop(name[5:])
                func(value, **func_args)

    # grid setting
    if args.g:
        for key in attrs:
            if key=='ax' or (key.startswith('ax') and int(key[2:]) >= 0):
                attrs[key].grid()

    if args.grid:
        for grid_arg in args.grid:
            if grid_arg:
                ax, arg = _get_axis(grid_arg)
                grid = arg.format(**attrs)
                teye_eval('%s.grid(%s)'%(ax, grid), l=attrs)

    # legend setting 
    if args.l:
        for key in attrs:
            if key=='ax' or (key.startswith('ax') and int(key[2:]) >= 0):
                attrs[key].legend()

    if args.legend:
        for legend_arg in args.legend:
            if legend_arg:
                ax, arg = _get_axis(legend_arg)
                legend = arg.format(**attrs)
                teye_eval('%s.legend(%s)'%(ax, legend), l=attrs)

def teye_plot(args, attrs):

    # matplotlib settings

    # pages setting
    if args.pages:
        arglist = args.pages.split(',', 1)
        attrs['num_pages'] = int(arglist[0])
        if len(arglist) > 1:
            page_args = parse_kwargs({}, arglist[1], attrs)
            if 'page_names' in page_args:
                attrs['page_names'] = page_args['page_names']
            if 'pdf_merge' in page_args and page_args['pdf_merge']:
                from matplotlib.backends.backend_pdf import PdfPages
                attrs['_pdf_merge'] = PdfPages
    else:
        attrs['num_pages'] = 1

    for idx in range(attrs['num_pages']):

        attrs['page_num'] = idx

        # figure setting
        if args.figure:
            attrs['figure'] = teye_eval('pyplot.figure(%s)'%args.figure, l=attrs)
        else:
            attrs['figure'] = attrs['pyplot'].figure()


        # plot axis
        if args.ax:
            for ax_arg in args.ax:
                axname, others = _get_axis(ax_arg, delimiter='=')
                if axname:
                    attrs[axname] = teye_eval('figure.add_subplot(%s)'%others, l=attrs)
                else:
                    raise UsageError('Wrong axis option: %s'%ax_arg)
        else:
            attrs['ax'] = attrs['figure'].add_subplot(111)

        # page names
        if 'page_names' in attrs:
            page_names = attrs['page_names']
            if callable(page_names):
                attrs['page_name'] = page_names(attrs['page_num'])
            else:
                attrs['page_name'] = page_names[attrs['page_num']]
        else:
            attrs['page_name'] = 'page%d'%(attrs['page_num'] + 1)

        # generate plots
        gen_plot(args, attrs)

        # selected axes functions
        axes_main_functions(args, attrs)

        # execute axes functions
        for axes_arg in args.axes:
            ax, arg = _get_axis(axes_arg)
            axes = arg.split(',', 1)
            if len(axes) == 1:
                teye_eval('ax.%s()'%axes[0], l=attrs)
            else:
                teye_eval('%s.%s(%s)'%(ax, axes[0], axes[1]), l=attrs)

        if not args.axes and not attrs['plots']:
            if len(attrs['_data_objects']) > 0:
                for data_obj in attrs['_data_objects']:
                    attrs['ax'].plot(data_obj.get_data('', '', attrs))
            else:
                error_exit("There is no data to plot.")

        # saving an image file
        if args.save:
            for saveargs in args.save:
                arglist = saveargs.split(',', 1)
                if '_pdf_merge' in attrs:
                    if '_pdf_pages' not in attrs:
                        teye_exec('_pdf_pages = _pdf_merge(%s)'%arglist[0], l=attrs)
                    teye_exec('_pdf_pages.savefig()', l=attrs)
                else:
                    teye_exec('pyplot.savefig(%s)'%saveargs, l=attrs)

        # displyaing an image on screen
        if not args.noshow:
            attrs['pyplot'].show()

            attrs['pyplot'].close()

    # multi-page closing
    if '_pdf_pages' in attrs:
        attrs['_pdf_pages'].close()
