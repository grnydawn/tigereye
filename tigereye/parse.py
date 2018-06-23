# -*- coding: utf-8 -*-
"""tigereye argument parsing module."""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import shlex
import argparse

class ArgParse(object):

    def __init__(self, argv):

        self._template, newargv = self._handle_template(argv)
        self._args = self._parse_arguments(newargv)

    def usage(self):
        return 'Usage: T.B.D.'

    def __str__(self):
        l = [str(self._args)]
        l.append(str(self._template))
        return '\n'.join(l)

    def __getattr__(self, name):

        if name in self._args:
            if self._args[name] is None:
                if self._template is not None:
                    return getattr(self._template, name)
            else:
                return self._args[name]
            return None

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

    def _extract_argument(self, argv, *extract):

        if len(argv) < 2:
            return [], argv

        extracts = [];
        newargv = []
        skip = False

        for arg, nextarg in zip(argv, argv[1:]+[None]):

            if skip:
                skip = False
                continue

            if arg in extract:
                extracts.append(nextarg)
                skip = True
            else:
                newargv.append(arg)

        return extracts, newargv

    def _load_template(self, template):

        lines = []
        with open(template, 'rb') as f:
            for line in f:
                line = line.strip()
                if line and line[-1] == '\\':
                    line = line[:-1]
                lines.append(line)

        cmdline = ' '.join(lines)
        return teye_parse(shlex.split(cmdline), None)

    def _handle_template(self, argv):

        template, newargv = self._extract_argument(argv, "-i", "--import")
        if len(template) > 1:
            error_exit('More than one templates are imported.')
        elif len(template) == 1:
            return self._load_template(template[0]), newargv
        else:
            return None, newargv

    def _parse_arguments(self, argv):

        parser = argparse.ArgumentParser(description='A reusable data-manipulation and plotting tool')
        parser.add_argument('data_sources', metavar='data source', nargs='*', help='input raw data.')
        parser.add_argument('-v', '--variable', metavar='varname:<formula>', action='append', help='define data.')
        parser.add_argument('-t', '--title', metavar='title', action='append', help='title  plotting.')
        parser.add_argument('-p', '--plot', metavar='plot type', action='append', help='plot type for plotting.')
        parser.add_argument('-f', '--figure', metavar='figure', help='figure for plotting.')
        parser.add_argument('-s', '--save', metavar='save', action='append', help='file path to save png image.')
        parser.add_argument('-d', '--value', metavar='value', action='append', help='print data value on screen.')
        parser.add_argument('-x', '--xaxis', metavar='xaxis', action='append', help='axes function wrapper for x axis settings.')
        parser.add_argument('-y', '--yaxis', metavar='yaxis', action='append', help='axes function wrapper for y axis settings.')
        parser.add_argument('-z', '--zaxis', metavar='zaxis', action='append', help='axes function wrapper for z axis settings.')
        parser.add_argument('-g', action='store_true', help='grid for ax plotting.')
        parser.add_argument('-l', action='store_true', help='legend for ax plotting')
        parser.add_argument('--legend', metavar='legend', action='append', help='plot legend')
        parser.add_argument('--grid', metavar='grid', action='append', help='grid for plotting.')
        parser.add_argument('--ax', metavar='ax', action='append', help='define plot axes.')
        parser.add_argument('--axes', metavar='axes', action='append', help='define Axes function.')
        parser.add_argument('--data-format', metavar='data format', action='append', help='define the format and load options of raw input data.')
        parser.add_argument('--calc', metavar='calc', action='append', help='python code for manipulating data.')
        parser.add_argument('--pages', metavar='pages', help='page settings.')
        parser.add_argument('--page-calc', metavar='page_calc', action='append', help='python code for manipulating data within page generation.')
        parser.add_argument('-i', '--import', metavar='template', help='importing a tigereye template')
        parser.add_argument('--import-page', metavar='page_template', action='append', help='page template')
        parser.add_argument('--import-data', metavar='data_template', action='append', help='data template')
        parser.add_argument('--noshow', action='store_true', default=False, help='prevent showing plot on screen.')
        parser.add_argument('--noplot', action='store_true', default=False, help='prevent generating plot.')
        parser.add_argument('--version', action='version', version='tigereye version 0.1.0')

        parsed_args = parser.parse_args(argv)

        return dict((k, v) for k, v in parsed_args._get_kwargs())


def teye_parse(argv, attrs):

    args = ArgParse(argv)

    return args
