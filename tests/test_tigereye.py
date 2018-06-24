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

def test_main():
    assert main(["[1,2,3]"]) == 0


def test_array_in_cmdline():
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
    assert main(argv) == 0

def test_numpy_data():
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
    assert main(argv) == 0

def test_numpy_text():
    argv = [
        "%s"%numpy_text_data1,
        "--data-format", "numpytext, delimiter=' '",
        "-v", "l1=d0[1,:]",
        "-p", "plot, l1**2",
        #"-d", "l1",
        #"--noplot",
    ]
    assert main(argv) == 0

def test_csv_file():
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
        #"--pages", "2, pdf_merge=True",
        #"--noplot",
        "--save", "'test.pdf'",

    ]
    assert main(argv) == 0

def test_axis_opt():
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
    assert main(argv) == 0

def test_axis_opt():
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
    assert main(argv) == 0


def test_remote_csv():
    argv = [
        "%s"%remote_csv_data1, "['Page1', 'Page2']",
        "-v", "l=d0",
        "-v", "l3=max(d0[1,:])",
        "-v", "l4=d1",
        "-p", "plot, l[page_num, :]**2",
        "-t", "l4[page_num]",
        "--data-format", "d0:numpytext, delimiter=','",
        #"--pages", "2",
        "--pages", "2, pdf_merge=True",
        #"--noplot",
        "--save", "'test.pdf'",

    ]
    assert main(argv) == 0

def test_template1():
    argv = [
        "-i", "%s"%template_sampel1,
        "-t", "'My Plot'",
    ]
    assert main(argv) == 0

