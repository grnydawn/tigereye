# -*- coding: utf-8 -*-
"""tigereye plotting module."""

from __future__ import (absolute_import, division,
    print_function, unicode_literals)

import re

from .error import UsageError
from .util import (error_exit, teye_eval, teye_exec, temp_attrs,
    parse_kwargs)

_re_ax = re.compile(r'(?P<ax>ax\d*)\s*:\s*(?P<others>.*)')

def _get_axis(arg):
    match = _re_ax.match(arg)
    if match:
        return match.group('ax'), match.group('others')
    else:
        return 'ax', arg

def gen_plot(args, attrs):

    # page names
    if 'page_names' in attrs:
        page_names = attrs['page_names']
        if callable(page_names):
            attrs['page_name'] = page_names(attrs['page_num'])
        else:
            attrs['page_name'] = page_names[attrs['page_num']]
    else:
        attrs['page_name'] = 'page%d'%(attrs['page_num'] + 1)

    # plotting
    plots = []
    plot_labels = []
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
                        if hasattr(p, 'get_label'):
                            plot_labels.append(p.get_label())
                        else:
                            plot_labels.append('N/A')
                except TypeError:
                    plots.append(plot_handle)
                    if hasattr(plot_handle, 'get_label'):
                        plot_labels.append(plot_handle.get_label())
                    else:
                        plot_labels.append('N/A')

                if pname == 'pie':
                    attrs[ax].axis('equal')
    else:
        if len(attrs['_data_objects']) > 0:
            for data_obj in attrs['_data_objects']:
                attrs['ax'].plot(data_obj.get_data('', '', attrs))
        else:
            error_exit("There is no data to plot.")
    attrs['plots'] = plots
    attrs['plot_labels'] = plot_labels

    # title setting
    #if args.title:
    for title_arg in args.title:
        ax, targ = _get_axis(title_arg)
        title = targ.format(**attrs)
        teye_exec('%s.set_title(%s)'%(ax, title), l=attrs)

    # x ax.s setting
    if args.xlim:
        teye_exec('ax.set_xlim(%s)'%args.xlim, l=attrs)

    if args.xlabel:
        xlabel = args.xlabel.format(**attrs)
        teye_exec('ax.set_xlabel(%s)'%xlabel, l=attrs)

    if args.xticks:
        teye_exec('ax.xticks(%s)'%args.xticks, l=attrs)

    if args.xtick_style:
        for xtick_style in args.xtick_style:
            if len(xtick_style.strip())==0: continue
            locs, labels = pyplot.xticks()
            teye_exec('ax.xticks(locs, %s)'%xtick_style, l=attrs)

    # y ax.s setting
    if args.ylim:
        teye_exec('ax.set_ylim(%s)'%args.ylim, l=attrs)

    if args.ylabel:
        ylabel = args.ylabel.format(**attrs)
        teye_exec('ax.set_ylabel(%s)'%ylabel, l=attrs)

    if args.yticks:
        teye_exec('ax.yticks(%s)'%args.yticks, l=attrs)

    if args.ytick_style:
        for ytick_style in args.ytick_style:
            if len(ytick_style.strip())==0: continue
            locs, labels = pyplot.yticks()
            teye_exec('ax.yticks(locs, %s)'%ytick_style, l=attrs)

    # grid setting
    if args.grid:
        for g in args.grid:
            teye_exec('ax.grid(%s)'%g, l=attrs)

    # legend setting 
    if args.legend:
        teye_exec('ax.legend(%s)'%args.legend, l=attrs)

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

def teye_plot(args, attrs):

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
        if args.axis:
            for axis_arg in args.axis:
                ax, others = _get_axis(axis_arg)
                if ax:
                    attrs[ax] = teye_eval('figure.add_subplot(%s)'%others, l=attrs)
                else:
                    raise UsageError('Wrong axis option: %s'%axis_arg)
        else:
            attrs['ax'] = attrs['figure'].add_subplot(111)

        gen_plot(args, attrs)

        attrs['pyplot'].close()

    # multi-page closing
    if '_pdf_pages' in attrs:
        attrs['_pdf_pages'].close()
