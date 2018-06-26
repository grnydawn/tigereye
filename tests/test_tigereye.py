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
template_sampel1 = "%s/templates/sample1.tgr"%curdir

@pytest.fixture(scope="session")
def tempdir(tmpdir_factory):
    return tmpdir_factory.getbasetemp()

#def test_main():
#    assert main(["[1,2,3]"]) == 0

def _main(argv, tempdir):

    outfile = '%s/test.pdf'%tempdir
    if os.path.isfile(outfile):
        os.remove(outfile)

    argv.extend(["-s", "'%s'"%outfile, "--noshow"])
    #argv.extend(["-s", "'%s'"%outfile])
    main(argv)

    assert os.path.isfile(outfile)

def test_array_in_cmdline(tempdir):
    argv = [
        "[[1,2,3], [1,4,9]]", "[4,5,6]",
        "-v", "l1=d1",
        "-v", "l2=d0[1].log(l2**l1).sqrt(l2)",
        "-t", "'test', fontsize=24",
        "-x", "label='xlabel'",
        "-x", "ticks=l1",
        "-x", "ticklabels=['a', 'b', 'c']",
        "-y", "label='ylabel'",
        "-p", "plot, l1, l2",
    ]

    _main(argv, tempdir)

def test_numpy_data(tempdir):
    argv = [
        "-v", "l1=numpy.arange(3)",
        "-v", "l2=numpy.random~rand(3)",
        "-t", "'test', fontsize=24",
        "-x", "label='xlabel'",
        "-x", "ticklabels=['a', 'b', 'c']",
        "-y", "label='ylabel'",
        "-p", "scatter, l1, l2, label='s'",
        "-p", "scatter, l2, l1, label='t'",
        "-l",
    ]

    _main(argv, tempdir)

def test_numpy_text(tempdir):
    argv = [
        "%s"%numpy_text_data1,
        "--data-format", "numpytext, delimiter=' '",
        "-v", "l1=d0[1,:]",
        "-p", "plot, l1**2",
        #"-d", "l1",
        #"--noplot",
    ]

    _main(argv, tempdir)

def test_csv_file(tempdir):
    outfile = '%s/test.pdf'%tempdir
    argv = [
        "%s"%csv_text_data1,
        "-v", "l1=d0[1,:]",
        "-v", "l2=l1.astype(numpy.float)",
        "-v", "l3=max(d0[1,:])",
        "-p", "plot, l2**2",
        "--data-format", "csv, delimiter=';'",
        "--calc", "l2 = l2**2",
        "--value", "l2",
        "--pages", "2",
        "--book", "'%s', page_save=False"%outfile,
        #"--noplot",

    ]

    _main(argv, tempdir)

def test_axis_opt(tempdir):
    argv = [
        "[1,2,3]", "[4,5,6]",
        "-v", "l1=d0",
        "-v", "l2=d1",
        "-x", "label='xlabel', fontsize=20",
        "-x", "ticks=[1.5, 2.5]",
        "-x", "ticklabels=['a', 'b']",
        "-y", "label='ylabel'",
        "-y", "ticks=[4.5, 5.5]",
        "-y", "ticklabels=['x', 'y']",
        "--axes", "set_title, 'new title'",
        "-t", "'Title'",
        "-g",
        "-l",
        "-p", "plot, l1, l2, label='label'",
    ]

    _main(argv, tempdir)

def test_axis_opt(tempdir):
    argv = [
        "[1,2,3]", "[4,5,6]",
        "-v", "l1=d0",
        "-v", "l2=d1",
        "--ax", "ax1=121",
        "--ax", "ax2=122",
        "-x", "ax1:label='xlabel', fontsize=20",
        "-x", "ax2:ticks=[1.5, 2.5]",
        "-x", "ax1:ticklabels=['a', 'b']",
        "-y", "ax2:label='ylabel'",
        "-y", "ax1:ticks=[4.5, 5.5]",
        "-y", "ax2:ticklabels=['x', 'y']",
        "--axes", "ax1:set_title, 'new title'",
        "-t", "ax2:'Title'",
        "-l",
        "-p", "ax1:plot, l1, l2, label='label'",
        "-p", "ax2:plot, l2, l1, label='label'",
    ]

    _main(argv, tempdir)

def test_remote_csv(tempdir):
    outfile = '%s/test.pdf'%tempdir
    argv = [
        "%s"%remote_csv_data1, "['Page1', 'Page2']",
        "-v", "l=d0",
        "-v", "l3=max(d0[1,:])",
        "-v", "l4=d1",
        "-p", "plot, l[page_num, :]**2",
        "-t", "l4[page_num]",
        "--data-format", "d0:numpytext, delimiter=','",
        "--pages", "2",
        "--book", "'%s'"%outfile,
        #"--noplot",
    ]

    _main(argv, tempdir)

def test_template1(tempdir):
    argv = [
        "-i", "%s"%template_sampel1,
        "-t", "'My Plot'",
    ]

    _main(argv, tempdir)


def test_figure_text(tempdir):
    argv = [
        "--figure", "text, 0.5, 0.5, 'Hello World!'",
    ]

    _main(argv, tempdir)

def test_3D_line(tempdir):
    argv = [
        "--ax", "ax= projection='3d'",
        "-v", "theta=numpy.linspace(-4 * numpy.pi, 4 * numpy.pi, 100)",
        "-v", "z=numpy.linspace(-2, 2, 100)",
        "-v", "r=z**2 + 1",
        "-v", "x=r * numpy.sin(theta)",
        "-v", "y=r * numpy.cos(theta)",
        "-p", "ax: plot, x, y, z, label='parametric curve'",
        "-l",
    ]

    _main(argv, tempdir)

def test_page_calc(tempdir):
    outfile = '%s/test.pdf'%tempdir
    argv = [
        "-v", "i=numpy.linspace(0, 1)",
        "-p", "plot, i, j",
        "--page-calc", "j=i*10+page_num",
        "-t", "'Page-%d'%page_num",
        "--pages", "2",
        "--book", "'%s', page_save=True"%outfile,
    ]

    _main(argv, tempdir)

def test_import_data(tempdir):
    outfile = '%s/test.pdf'%tempdir
    argv = [
        "--import-data", "x:varx, y:vary = '%s'"%template_sampel1,
        "-p", "plot, x, y, label='line1'"
    ]

    _main(argv, tempdir)


def test_import_plot(tempdir):
    outfile = '%s/test.pdf'%tempdir
    argv = [
        "-v", "x=numpy.linspace(0, 2*numpy.pi)",
        "-v", "y=numpy.sin(x)",
        "--import-plot", "axlocal:ax = 111, '%s', varx=x, vary=y"%template_sampel1
    ]

    _main(argv, tempdir)

