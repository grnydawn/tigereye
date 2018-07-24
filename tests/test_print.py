#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `tigereye` package."""

import os
import sys
import pytest

from tigereye import main

curdir = os.path.dirname(os.path.realpath(__file__))

numpy_text_data1 = "%s/data/numpy_text_data1.csv"%curdir
csv_text_data1 = "%s/data/csv_text_data1.csv"%curdir
remote_csv_data1 = "https://raw.githubusercontent.com/grnydawn/tigereye/master/data/simple.csv"
local_function1 = "%s/function/sample1.py"%curdir
template_sample1 = "%s/templates/sample1.tgr"%curdir
folding_data1 = "%s/data/wetdepa.slope.csv"%curdir

def _main(argv, capsys):

    main(argv)

    outerr = capsys.readouterr()
    assert outerr.out and not outerr.err

def test_str(capsys):
    argv = [
        "print",
        "[[1,2,3], [1,4,9]]", "[4,5,6]",
        "--str", "D",
    ]

    _main(argv, capsys)

def test_pandas(capsys):
    argv = [
        "print",
        "[[1,2,3], [1,4,9]]", "[4,5,6]",
        "--head", "D[0].iloc[0]@2",
        "--head", "D[1]@2",
    ]

    _main(argv, capsys)


def test_folding(capsys):
    argv = [
        "print",
        folding_data1,
        "--data-format", "csv, delimiter=';', header=None",
        "--calc", "brcn=D.loc[D.iloc[:,2]=='PAPI_BR_CN',:]",
        "-s", "brcn",
        "--output", "x=brcn.iloc[:,3],y=brcn.iloc[:,4]"
    ]

    _main(argv, capsys)


#
#def ttest_numpy_data(tempdir):
#    argv = [
#        "numpy.arange(3)",
#        "numpy.random.rand(3)",
#        "-t", "'test', fontsize=24",
#        "-x", "label@'xlabel'",
#        "-x", "ticklabels@['a', 'b', 'c']",
#        "-y", "label@'ylabel'",
#        "-p", "scatter@ D[0].values, D[1].values, label='s'",
#        "-p", "scatter@ D[1].values, D[0].values, label='t'",
#        "-l",
#    ]
#
#    _main(argv, tempdir)
#
#def ttest_numpy_text(tempdir):
#    argv = [
#        "%s"%numpy_text_data1,
#        "--data-format", "csv, sep=' ', header=None",
#        "-p", "plot@ D.values**2",
#    ]
#
#    _main(argv, tempdir)
#
#def ttest_csv_file(tempdir):
#    outfile = '%s/test.pdf'%tempdir
#    argv = [
#        csv_text_data1,
#        "--calc", "l1=D.values",
#        "--calc", "l2=l1.astype(numpy.float)",
#        "--calc", "l3=max(D)",
#        "-p", "plot@ l2**(page_num+1)",
#        "--data-format", "csv, delimiter=';'",
#        "--pages", "2",
#        "--pdf-bind", "'%s'"%outfile,
#        #"--noplot",
#
#    ]
#
#    _main(argv, tempdir)
#
#def ttest_axis_opt(tempdir):
#    argv = [
#        "[1,2,3]", "[4,5,6]",
#        "--calc", "l1=D[0].values",
#        "--calc", "l2=D[1].values",
#        "-x", "label@'xlabel', fontsize=20",
#        "-x", "ticks@[1.5, 2.5]",
#        "-x", "ticklabels@['a', 'b']",
#        "-y", "label@'ylabel'",
#        "-y", "ticks@[4.5, 5.5]",
#        "-y", "ticklabels@['x', 'y']",
#        "--axes", "set_title@ 'new title'",
#        "-t", "'Title'",
#        "-g",
#        "-l",
#        "-p", "plot@ l1, l2, label='label'",
#    ]
#
#    _main(argv, tempdir)
#
#def ttest_axis_opt(tempdir):
#    argv = [
#        "[1,2,3]", "[4,5,6]",
#        "--calc", "l1=D[0].values",
#        "--calc", "l2=D[1].values",
#        "--ax", "ax1@121",
#        "--ax", "ax2@122",
#        "-x", "ax1, label@'lxabel', fontsize=20",
#        "-x", "ax2, ticks@[1.5, 2.5]",
#        "-x", "ax1, ticklabels@['a', 'b']",
#        "-y", "ax2, label@'ylabel'",
#        "-y", "ax1, ticks@[4.5, 5.5]",
#        "-y", "ax2, ticklabels@['x', 'y']",
#        "--axes", "ax1, set_title@'new title'",
#        "-t", "ax2@'Title'",
#        "-l",
#        "-p", "ax1, plot@l1, l2, label='label'",
#        "-p", "ax2, plot@l2, l1, label='label'",
#    ]
#
#    _main(argv, tempdir)
#
#def ttest_remote_csv(tempdir):
#    outfile = '%s/test.pdf'%tempdir
#    argv = [
#        remote_csv_data1, "['Page1', 'Page2']",
#        "--calc", "l=D",
#        "--calc", "l3=D[0].values",
#        "--calc", "l4=D[1]",
#        "-p", "plot@ l[0].values[page_num, :]**2",
#        "-t", "l4[page_num]",
#        "--data-format", "0@csv, delimiter=','",
#        "--pages", "2",
#        "--pdf-bind", "'%s'"%outfile,
#        #"--noplot",
#    ]
#
#    _main(argv, tempdir)
#
#def ttest_template1(tempdir):
#    argv = [
#        "numpy.linspace(0, 2*numpy.pi)",
#        "numpy.sin(D[0].values)",
#        "-i", "%s?name=sinplot@X=D[0].values, Y=D[1].values"%template_sample1,
#        "-t", "'My Plot'",
#    ]
#
#        #"-i", "%s?name=sinplot@X=D[0].values, Y=D[1].values"%template_sample1,
#    _main(argv, tempdir)
#
#
#def ttest_figure_text(tempdir):
#    argv = [
#        "[0.5, 0.5]",
#        "--figure", "text@ D[0], D[1], 'Hello World!'",
#        #"--figure", "text@ 0.5, 0.5, 'Hello World!'",
#    ]
#
#    _main(argv, tempdir)
#
#def ttest_3D_line(tempdir):
#    argv = [
#        "numpy.linspace(-4 * numpy.pi, 4 * numpy.pi, 100)",
#        "numpy.linspace(-2, 2, 100)",
#        "D[1]**2 + 1",
#        "D[2] * numpy.sin(D[0])",
#        "D[2] * numpy.cos(D[0])",
#        "--ax", "ax@ projection='3d'",
#        "-p", "ax, plot@D[3], D[4], D[2], label='parametric curve'",
#        "-l",
#    ]
#
#    _main(argv, tempdir)
#
#def ttest_page_calc(tempdir):
#    outfile = '%s/test.pdf'%tempdir
#    argv = [
#        "numpy.linspace(0, 1)",
#        "-p", "plot@D.values, j",
#        "--page-calc", "j=D.values*10+page_num",
#        "-t", "'Page-%d'%page_num",
#        "--pages", "2",
#        "--pdf-bind", "'%s'"%outfile,
#    ]
#
#    _main(argv, tempdir)
#
#
#def ttest_pdf_bind(tempdir):
#    outfile = '%s/test.pdf'%tempdir
#    argv = [
#        "numpy.linspace(0, 1)",
#        "--pdf-bind", "'%s'"%outfile,
#        "-p", "plot@D.values, j",
#        "--page-calc", "j=D.values*10+page_num",
#        "-t", "'Page-%d'%page_num",
#        "--pages", "2",
#        "->", "plot",
#        "-i", "%s?name=sinplot@X=D.values, Y=numpy.linspace(1,2)"%template_sample1,
#    ]
#
#    _main(argv, tempdir)
#
#def test_folding(tempdir):
#    outfile = '%s/test.pdf'%tempdir
#    argv = [
#        folding_data1,
#        "--data-format", "csv, delimiter=';'",
#        "--pdf-bind", "'%s'"%outfile,
#        #"-p", "plot@D.values, j",
#        #"--page-calc", "j=D.values*10+page_num",
#        #"-t", "'Page-%d'%page_num",
#        #"--pages", "2",
#        #"->", "plot",
#        #"-i", "%s?name=sinplot@X=D.values, Y=numpy.linspace(1,2)"%template_sample1,
#    ]
#
#    _main(argv, tempdir)
