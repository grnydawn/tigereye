# -*- coding: utf-8 -*-
"""tigereye plotting module."""

from __future__ import (absolute_import, division,
    print_function, unicode_literals)

import re

from .error import UsageError
from .util import (error_exit, teye_eval, parse_funcargs, get_var)

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
        return arg, ''

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
                plot_handle = teye_eval('%s.%s(%s)'%(ax, pname, pargs), attrs)

                try:
                    for p in plot_handle:
                        plots.append(p)
                except TypeError:
                    plots.append(plot_handle)

                if pname == 'pie':
                    attrs[ax].axis('equal')

    attrs['plots'] = plots

def axes_main_functions(args, attrs):

    # title setting
    if args.title:
        for title_arg in args.title:
            ax, title = _get_axis(title_arg)
            teye_eval('%s.set_title(%s)'%(ax, title), attrs)


    # x-axis setting
    if args.xaxis:
        for xaxis_arg in args.xaxis:
            ax, xaxis = _get_axis(xaxis_arg)

            set_xfuncs =  dict((x, getattr(attrs[ax], x)) for x in dir(attrs[ax]) if x.startswith('set_x'))
            vargs, kwargs = parse_funcargs(xaxis, attrs)

            for name, func in set_xfuncs.items():
                funckey = name[5:] # set_x functions
                if funckey in kwargs:
                    func_args = dict(kwargs)
                    value = func_args.pop(funckey)
                    func(value, **func_args)

    # y-axis setting
    if args.yaxis:
        for yaxis_arg in args.yaxis:
            ax, yaxis = _get_axis(yaxis_arg)

            set_yfuncs =  dict((y, getattr(attrs[ax], y)) for y in dir(attrs[ax]) if y.startswith('set_y'))
            vargs, kwargs = parse_funcargs(yaxis, attrs)

            for name, func in set_yfuncs.items():
                funckey = name[5:]
                if funckey in kwargs:
                    func_args = dict(kwargs)
                    value = func_args.pop(funckey)
                    func(value, **func_args)

    # z-axis setting
    if args.zaxis:
        for zaxis_arg in args.zaxis:
            ax, zaxis = _get_axis(zaxis_arg)

            set_zfuncs =  dict((z, getattr(attrs[ax], z)) for z in dir(attrs[ax]) if z.startswith('set_z'))
            vargs, kwargs = parse_funcargs(zaxis, attrs)

            for name, func in set_zfuncs.items():
                funckey = name[5:]
                if funckey in kwargs:
                    func_args = dict(kwargs)
                    value = func_args.pop(funckey)
                    func(value, **func_args)

    # grid setting
    if args.g:
        for key in attrs:
            if key=='ax' or (key.startswith('ax') and int(key[2:]) >= 0):
                attrs[key].grid()

    if args.grid:
        for grid_arg in args.grid:
            if grid_arg:
                ax, grid = _get_axis(grid_arg)
                teye_eval('%s.grid(%s)'%(ax, grid), attrs)

    # legend setting 
    if args.l:
        for key in attrs:
            if key=='ax' or (key.startswith('ax') and int(key[2:]) >= 0):
                attrs[key].legend()

    if args.legend:
        for legend_arg in args.legend:
            if legend_arg:
                ax, legend = _get_axis(legend_arg)
                teye_eval('%s.legend(%s)'%(ax, legend), attrs)

def teye_plot(args, attrs):

    # matplotlib settings
    # pages setting
    if args.pages:
        vargs, kwargs = parse_funcargs(args.pages, attrs)

        if vargs:
            attrs['num_pages'] = vargs[-1]
        else:
            attrs['num_pages'] = 1

        for key, value in kwargs.items():
            if key == 'pdf_merge' and value:
                from matplotlib.backends.backend_pdf import PdfPages
                attrs['_pdf_merge'] = PdfPages
            else:
                attrs[key] = value
    else:
        attrs['num_pages'] = 1

    for idx in range(attrs['num_pages']):

        attrs['page_num'] = idx

        if args.page_calc:
            for vname, formula in get_var(args.page_calc):
                attrs[vname] = teye_eval(formula, attrs)


        # figure setting
        if args.f:
            attrs['figure'] = teye_eval('pyplot.figure(%s)'%args.f, attrs)
        else:
            attrs['figure'] = attrs['pyplot'].figure()


        # import plot
        if args.import_plot:
            # add_subplot for the imported plot
            # --import-plot "axlocal: 321, http://dfsd.sdfs.fsd.sf.df.sdf, axremote, local1=remote1,local2=remote2, ..."
            import pdb; pdb.set_trace()

        # plot axis
        if args.ax:
            for ax_arg in args.ax:
                axname, others = _get_axis(ax_arg, delimiter='=')
                if axname:
                    vargs, kwargs = parse_funcargs(others, attrs)
                    if 'projection' in kwargs and kwargs['projection'] == '3d':
                         from mpl_toolkits.mplot3d import Axes3D
                         attrs['Axes3D'] = Axes3D
                    if len(vargs) == 0 or not isinstance(vargs[0], int):
                        attrs[axname] = teye_eval('figure.add_subplot(111, %s)'%others, attrs)
                    else:
                        attrs[axname] = teye_eval('figure.add_subplot(%s)'%others, attrs)
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

        # execute figure functions
        if args.figure:
            for fig_arg in args.figure:
                name, others = _get_name(fig_arg)
                if others:
                    teye_eval('figure.%s(%s)'%(name, others), attrs)
                else:
                    teye_eval('figure.%s()'%name, attrs)

        # generate plots
        gen_plot(args, attrs)

        # selected axes functions
        axes_main_functions(args, attrs)

        # execute axes functions
        if args.axes:
            for axes_arg in args.axes:
                ax, arg = _get_axis(axes_arg)
                name, others = _get_name(arg)
                if others:
                    teye_eval('%s.%s(%s)'%(ax, name, others), attrs)
                else:
                    teye_eval('ax.%s()'%name, attrs)
        elif not attrs['plots']:
            if len(attrs['_data_objects']) > 0:
                for data_obj in attrs['_data_objects']:
                    attrs['ax'].plot(data_obj.get_data('', '', attrs))
            elif not args.figure:
                error_exit("There is no data to plot.")

        # saving an image file
        if args.save:
            for save_arg in args.save:
                name, others = _get_name(save_arg)
                if '_pdf_merge' in attrs:
                    if '_pdf_pages' not in attrs:
                        attrs['_pdf_pages'] =  teye_eval('_pdf_merge(%s)'%name, attrs)
                    teye_eval('_pdf_pages.savefig()', attrs)
                else:
                    teye_eval('figure.savefig(%s)'%save_arg, attrs)

        # displyaing an image on screen
        if not args.noshow:
            attrs['pyplot'].show()

        teye_eval('pyplot.close(figure)', attrs)

    # multi-page closing
    if '_pdf_pages' in attrs:
        attrs['_pdf_pages'].close()
