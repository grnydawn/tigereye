# -*- coding: utf-8 -*-
"""tigereye argument parsing module."""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import argparse

NUM_XINPUTS = 5
NUM_YINPUTS = 5
NUM_ZINPUTS = 5

class ArgParse(object):

    def __init__(self, argv):

        self._templates, newargv = self._handle_templates(argv)
        self._args = self._parse_arguments(newargv)

    def usage(self):
        return 'Usage: T.B.D.'

    def __str__(self):
        l = [str(self._args)]
        l.extend([str(t) for t in self._templates])
        return '\n'.join(l)

    def __getattr__(self, name):

        if name in self._args:
            return self._args[name]

        for template in self._templates:
            if hasattr(template, name):
                return getattr(template, name)

        raise AttributeError(
            "AttributeError: 'ArgParse' object has no attribute '%s'"%name)

    def __contains__(self, name):

        try:
            getattr(self, name)
            return True
        except AttributeError:
            return False

    def __getitem__(self, name):
        return getattr(self, name)

    def _extract_argument(self, argv, extract):

        if len(argv) < 2:
            return [], argv

        extracts = [];
        newargv = []
        skip = False

        for arg, nextarg in zip(argv, argv[1:]+[None]):

            if skip:
                skip = False
                continue

            if arg == extract:
                extracts.append(nextarg)
                skip = True
            else:
                newargv.append(arg)

        return extracts, newargv


    def _handle_templates(self, argv):

        templates, newargv = self._extract_argument(argv, "--template")
        return [self._load_template(t) for t in templates], newargv

    def _parse_arguments(self, argv):

        # number of x and y variables
        num_xinputs, newargv = self._extract_argument(argv, "--num-xinputs")
        num_yinputs, newargv = self._extract_argument(newargv, "--num-yinputs")
        num_zinputs, newargv = self._extract_argument(newargv, "--num-zinputs")
        num_xinputs = int(num_xinputs[-1]) if num_xinputs else NUM_XINPUTS
        num_yinputs = int(num_yinputs[-1]) if num_yinputs else NUM_YINPUTS
        num_zinputs = int(num_zinputs[-1]) if num_zinputs else NUM_ZINPUTS

        parser = argparse.ArgumentParser(description='A template-based data plotter')
        parser.add_argument('data_sources', metavar='data source', nargs='*', help='input raw data.')
        parser.add_argument('-x', metavar='<formula>', help='define data for x axis.')
        parser.add_argument('-y', metavar='<formula>', help='define data for left y axis.')
        parser.add_argument('-z', metavar='<formula>', help='define data for left z axis.')
        parser.add_argument('-t', '--title', metavar='title', action='append', default=[], help='title  plotting.')
        parser.add_argument('-p', '--plot', metavar='plot type', action='append', help='plot type for plotting.')
        parser.add_argument('-f', '--figure', metavar='figure', help='figure for plotting.')
        parser.add_argument('-g', '--grid', metavar='grid', nargs='?', const='b=True', action='append', help='grid for plotting.')
        parser.add_argument('-s', '--save', metavar='save', action='append', help='file path to save png image.')
        parser.add_argument('-l', '--legend', metavar='legend', nargs='?', const="plots, plot_labels, loc='best'", help='plot legend')
        parser.add_argument('-v', '--value', metavar='value', action='append', help='print data value on screen.')
        parser.add_argument('--axis', metavar='axis', action='append', help='define plot axes.')
        parser.add_argument('--data-format', metavar='data format', action='append', help='define the format and load options of raw input data.')
        parser.add_argument('--num-xinputs', metavar='number of xinputs', type=int, default=num_xinputs, help='set the number of x inputs.')
        parser.add_argument('--num-yinputs', metavar='number of yinputs', type=int, default=num_yinputs, help='set the number of y inputs.')
        parser.add_argument('--num-zinputs', metavar='number of zinputs', type=int, default=num_zinputs, help='set the number of z inputs.')
        parser.add_argument('--calc', metavar='calculation', action='append', help='python code.')
        parser.add_argument('--pages', metavar='pages', default='1', help='page settings.')
        parser.add_argument('--xlabel', metavar='x-label',  help='xlabel for plotting.')
        parser.add_argument('--xticks', metavar='x-ticks', help='xticks for plotting.')
        parser.add_argument('--xtick_style', metavar='x-tick style', action='append', help='xtick label style.')
        parser.add_argument('--xlim', metavar='x-tick range', help='xlim for plotting.')
        parser.add_argument('--ylabel', metavar='y-label', help='ylabel for plotting.')
        parser.add_argument('--yticks', metavar='y-ticks', help='yticks for plotting.')
        parser.add_argument('--ytick_style', metavar='y-tick style', action='append', help='ytick label style.')
        parser.add_argument('--ylim', metavar='y-tick range', help='ylim for plotting.')
        parser.add_argument('--zlabel', metavar='z-label',  help='zlabel for plotting.')
        parser.add_argument('--zticks', metavar='z-ticks', help='zticks for plotting.')
        parser.add_argument('--ztick_style', metavar='z-tick style', action='append', help='ztick label style.')
        parser.add_argument('--zlim', metavar='z-tick range', help='zlim for plotting.')
        parser.add_argument('--template', metavar='template', action='append', help='tigereye template')
        parser.add_argument('--page-template', metavar='page_template', action='append', help='page template')
        parser.add_argument('--data-template', metavar='data_template', action='append', help='data template')
        parser.add_argument('--noshow', action='store_true', default=False, help='prevent showing plot on screen.')
        parser.add_argument('--noplot', action='store_true', default=False, help='prevent generating plot.')
        parser.add_argument('--version', action='version', version='tigereye version 0.1.0')

        for idx in range(2, num_xinputs+1):
            parser.add_argument('--x%d'%idx, metavar='<formula>', help='define x%d data.'%idx)

        for idx in range(2, num_yinputs+1):
            parser.add_argument('--y%d'%idx, metavar='<formula>', help='define y%d data.'%idx)

        for idx in range(2, num_zinputs+1):
            parser.add_argument('--z%d'%idx, metavar='<formula>', help='define z%d data.'%idx)

        parsed_args = parser.parse_args(newargv)

        return dict((k, v) for k, v in parsed_args._get_kwargs())


def teye_parse(argv, attrs):

    args = ArgParse(argv)

    return args
