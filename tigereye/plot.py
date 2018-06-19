# -*- coding: utf-8 -*-
"""tigereye plotting module."""

from __future__ import (absolute_import, division,
    print_function, unicode_literals)

from .error import UsageError
from .util import error_exit, teye_eval, teye_exec, temp_attrs

def _pages_args(num_pages, page_names=None, pdf_merge=None):
    return num_pages, page_names, pdf_merge

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
            plotarg = plot.strip()
            poscomma = plotarg.find(',')
            if poscomma<0:
                raise UsageError('Wrong plot option: %s'%plotarg)
            else:
                pname = plotarg[:poscomma]
                pargs = plotarg[poscomma+1:]
                plot_handle = teye_eval('_ax.%s(%s)'%(pname, pargs), l=attrs)

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
                    attrs['_ax'].axis('equal')
    else:
        if len(attrs['_data_objects']) > 0:
            for data_obj in attrs['_data_objects']:
                attrs['_ax'].plot(data_obj.get_data('', '', attrs))
        else:
            error_exit("No plot is specified with -p or --plot flag.")
    attrs['plots'] = plots
    attrs['plot_labels'] = plot_labels

    # title setting
    if args.title:
        title = args.title.format(**attrs)
        teye_exec('_ax.set_title(%s)'%title, l=attrs)

    # x _ax.s setting
    if args.xlim:
        teye_exec('_ax.set_xlim(%s)'%args.xlim, l=attrs)

    if args.xlabel:
        xlabel = args.xlabel.format(**attrs)
        teye_exec('_ax.set_xlabel(%s)'%xlabel, l=attrs)

    if args.xticks:
        teye_exec('pyplot.xticks(%s)'%args.xticks, l=attrs)

    if args.xtick_style:
        for xtick_style in args.xtick_style:
            if len(xtick_style.strip())==0: continue
            locs, labels = pyplot.xticks()
            teye_exec('pyplot.xticks(locs, %s)'%xtick_style, l=attrs)

    # y _ax.s setting
    if args.ylim:
        teye_exec('_ax.set_ylim(%s)'%args.ylim, l=attrs)

    if args.ylabel:
        ylabel = args.ylabel.format(**attrs)
        teye_exec('_ax.set_ylabel(%s)'%ylabel, l=attrs)

    if args.yticks:
        teye_exec('pyplot.yticks(%s)'%args.yticks, l=attrs)

    if args.ytick_style:
        for ytick_style in args.ytick_style:
            if len(ytick_style.strip())==0: continue
            locs, labels = pyplot.yticks()
            teye_exec('pyplot.yticks(locs, %s)'%ytick_style, l=attrs)

    # grid setting
    if args.grid:
        for g in args.grid:
            teye_exec('_ax.grid(%s)'%g, l=attrs)

    # legend setting 
    if args.legend:
        teye_exec('pyplot.legend(%s)'%args.legend, l=attrs)

    # saving an image file
    if args.save:
        for saveargs in args.save:
            arglist = saveargs.split(',', 1)
            if '_pdf_merge' in attrs:
                if '_pdf_pages' not in attrs:
                    attrs['_pdf_pages'] = attrs['_pdf_merge'](arglist[0])
                #teye_exec('_pdf_pages.savefig(%s)'%''.join(arglist[1:]), l=attrs)
                teye_exec('_pdf_pages.savefig()', l=attrs)
            else:
                teye_exec('pyplot.savefig(%s)'%saveargs, l=attrs)

            #from matplotlib.backends.backend_pdf import PdfPages
            #attrs['_pdf_merge'] = PdfPages

    # displyaing an image on screen
    if not args.noshow:
        attrs['pyplot'].show()

def gen_figure(args, attrs):

    # figure setting
    if args.figure:
        attrs['figure'] = teye_eval('pyplot.figure(%s)'%args.figure, l=attrs)
    else:
        attrs['figure'] = attrs['pyplot'].figure()

    # plot axis
    attrs['_ax'] = attrs['figure'].add_subplot(111)

    # pages setting
    if args.pages:
        pnum, pnames, pdfmerge = teye_eval('_p(%s)'%args.pages,
            l=temp_attrs(attrs, [('_p', _pages_args)]))
        attrs['num_pages'] = int(pnum)
        if pnames:
            attrs['page_names'] = pnames
        if pdfmerge:
            attrs['_pdf_merge'] = pdfmerge
    else:
        attrs['num_pages'] = 1

def teye_plot(args, attrs):

    # figure and multi-page setting
    gen_figure(args, attrs)

    # page creation
    for pagenum in range(attrs['num_pages']):

        attrs['page_num'] = pagenum

        # plotting
        gen_plot(args, attrs)

        attrs['pyplot'].cla()

    # multi-page closing
    if '_pdf_pages' in attrs:
        attrs['_pdf_pages'].close()

    attrs['pyplot'].close()

