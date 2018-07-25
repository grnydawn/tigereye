#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `tigereye` package."""

import os
import sys
import pytest

from tigereye import main

curdir = os.path.dirname(os.path.realpath(__file__))

numpy_text_data1 = os.path.join(curdir, "data", "numpy_text_data1.csv")
csv_text_data1 = os.path.join(curdir, "data", "csv_text_data1.csv")
remote_csv_data1 = "https://raw.githubusercontent.com/grnydawn/tigereye/master/data/simple.csv"
local_function1 = os.path.join(curdir, "function", "sample1.py")
template_sample1 = os.path.join(curdir, "templates", "sample1.tgr")
folding_data1 = os.path.join(curdir, "data", "wetdepa.slope.csv")

@pytest.fixture(scope="session")
def tempdir(tmpdir_factory):
    return tmpdir_factory.getbasetemp()

#def test_main():
#    assert main(["[1,2,3]"]) == 0

def _main(argv, tempdir):

    outfile = tempdir.join('test.pdf')
    if outfile.isfile():
        os.remove(str(outfile))

    argv.extend(["-s", "'%s'"%outfile, "--noshow"])
    #argv.extend(["-s", "r'%s'"%outfile])
    main(argv)

    assert outfile.isfile()

def test_array_in_cmdline(tempdir):
    argv = [
        "[[1,2,3], [1,4,9]]", "[4,5,6]",
        "--calc", "l1=D[1]",
        "--calc", "l2=D[0].loc[0]*D[0].loc[1]",
        "-t", "'test', fontsize=24",
        "-x", "label@'xlabel'",
        "-x", "ticks@l1",
        "-x", "ticklabels@['a', 'b', 'c']",
        "-y", "label@'ylabel'",
        "-p", "plot@ l1, l2",
    ]

    _main(argv, tempdir)

def test_numpy_data(tempdir):
    argv = [
        "numpy.arange(3)",
        "numpy.random.rand(3)",
        "-t", "'test', fontsize=24",
        "-x", "label@'xlabel'",
        "-x", "ticklabels@['a', 'b', 'c']",
        "-y", "label@'ylabel'",
        "-p", "scatter@ D[0].values, D[1].values, label='s'",
        "-p", "scatter@ D[1].values, D[0].values, label='t'",
        "-l",
    ]

    _main(argv, tempdir)

def test_numpy_text(tempdir):
    argv = [
        "%s"%numpy_text_data1,
        "--data-format", "csv, sep=' ', header=None",
        "-p", "plot@ D.values**2",
    ]

    _main(argv, tempdir)

def test_csv_file(tempdir):
    outfile = tempdir.join('test.pdf')
    argv = [
        csv_text_data1,
        "--calc", "l1=D.values",
        "--calc", "l2=l1.astype(numpy.float)",
        "--calc", "l3=max(D)",
        "-p", "plot@ l2**(page_num+1)",
        "--data-format", "csv, delimiter=';'",
        "--pages", "2",
        "--pdf-bind", "'%s'"%outfile,
        #"--noplot",

    ]

    _main(argv, tempdir)

def test_axis_opt(tempdir):
    argv = [
        "[1,2,3]", "[4,5,6]",
        "--calc", "l1=D[0].values",
        "--calc", "l2=D[1].values",
        "-x", "label@'xlabel', fontsize=20",
        "-x", "ticks@[1.5, 2.5]",
        "-x", "ticklabels@['a', 'b']",
        "-y", "label@'ylabel'",
        "-y", "ticks@[4.5, 5.5]",
        "-y", "ticklabels@['x', 'y']",
        "--axes", "set_title@ 'new title'",
        "-t", "'Title'",
        "-g",
        "-l",
        "-p", "plot@ l1, l2, label='label'",
    ]

    _main(argv, tempdir)

def test_axis_opt(tempdir):
    argv = [
        "[1,2,3]", "[4,5,6]",
        "--calc", "l1=D[0].values",
        "--calc", "l2=D[1].values",
        "--ax", "ax1@121",
        "--ax", "ax2@122",
        "-x", "ax1, label@'lxabel', fontsize=20",
        "-x", "ax2, ticks@[1.5, 2.5]",
        "-x", "ax1, ticklabels@['a', 'b']",
        "-y", "ax2, label@'ylabel'",
        "-y", "ax1, ticks@[4.5, 5.5]",
        "-y", "ax2, ticklabels@['x', 'y']",
        "--axes", "ax1, set_title@'new title'",
        "-t", "ax2@'Title'",
        "-l",
        "-p", "ax1, plot@l1, l2, label='label'",
        "-p", "ax2, plot@l2, l1, label='label'",
    ]

    _main(argv, tempdir)

def test_remote_csv(tempdir):
    outfile = tempdir.join('test.pdf')
    argv = [
        remote_csv_data1, "['Page1', 'Page2']",
        "--calc", "l=D",
        "--calc", "l3=D[0].values",
        "--calc", "l4=D[1]",
        "-p", "plot@ l[0].values[page_num, :]**2",
        "-t", "l4[page_num]",
        "--data-format", "0@csv, delimiter=','",
        "--pages", "2",
        "--pdf-bind", "'%s'"%outfile,
        #"--noplot",
    ]

    _main(argv, tempdir)

def test_template1(tempdir):
    argv = [
        "numpy.linspace(0, 2*numpy.pi)",
        "numpy.sin(D[0].values)",
        "-i", "%s?name=sinplot@X=D[0].values, Y=D[1].values"%template_sample1,
        "-t", "'My Plot'",
    ]

        #"-i", "%s?name=sinplot@X=D[0].values, Y=D[1].values"%template_sample1,
    _main(argv, tempdir)


def test_figure_text(tempdir):
    argv = [
        "[0.5, 0.5]",
        "--figure", "text@ D[0], D[1], 'Hello World!'",
        #"--figure", "text@ 0.5, 0.5, 'Hello World!'",
    ]

    _main(argv, tempdir)

def test_3D_line(tempdir):
    argv = [
        "numpy.linspace(-4 * numpy.pi, 4 * numpy.pi, 100)",
        "numpy.linspace(-2, 2, 100)",
        "D[1]**2 + 1",
        "D[2] * numpy.sin(D[0])",
        "D[2] * numpy.cos(D[0])",
        "--ax", "ax@ projection='3d'",
        "-p", "ax, plot@D[3], D[4], D[2], label='parametric curve'",
        "-l",
    ]

    _main(argv, tempdir)

def test_page_calc(tempdir):
    outfile = tempdir.join('test.pdf')
    argv = [
        "numpy.linspace(0, 1)",
        "-p", "plot@D.values, j",
        "--page-calc", "j=D.values*10+page_num",
        "-t", "'Page-%d'%page_num",
        "--pages", "2",
        "--pdf-bind", "'%s'"%outfile,
    ]

    _main(argv, tempdir)


def test_pdf_bind(tempdir):
    outfile = tempdir.join('test.pdf')
    argv = [
        "numpy.linspace(0, 1)",
        "--pdf-bind", "'%s'"%outfile,
        "-p", "plot@D.values, j",
        "--page-calc", "j=D.values*10+page_num",
        "-t", "'Page-%d'%page_num",
        "--pages", "2",
        "->", "plot",
        "-i", "%s?name=sinplot@X=D.values, Y=numpy.linspace(1,2)"%template_sample1,
    ]

    _main(argv, tempdir)

def test_folding(tempdir):
    outfile = tempdir.join('test.pdf')
    argv = [
        folding_data1,
        "--data-format", "csv, delimiter=';'",
        "--pdf-bind", "'%s'"%outfile,
        "--data-format", "csv, delimiter=';', header=None",
        "--calc", "hwcs=D.iloc[:,2].drop_duplicates().values",
        "--pages", "len(hwcs)",
        "--page-calc", "HWC=D.loc[D.iloc[:,2]==hwcs[page_num],:]",
        "-p", "plot@HWC.iloc[:,3].values, HWC.iloc[:,4].values",
        "-t", "hwcs[page_num]",
        "-x", "label@'elapsed time(0: start, 1: end)'",
        "-y", "label@'event'",
    ]

    _main(argv, tempdir)
