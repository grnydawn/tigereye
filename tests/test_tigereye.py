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

def ttest_main():
    assert main(["[1,2,3]"]) == 0


def ttest_array_in_cmdline():
    argv = [
        "[[1,2,3], [1,4,9]]", "[4,5,6]",
        "-x", "d1",
        "-y", "d0[1].log(y**x).sqrt(y)",
        "-t", "'test', fontsize=24",
        "--xlabel", "'xlabel'",
        "--xticks", "x, ['a', 'b', 'c']",
        "--ylabel", "'ylabel'",
        "-p", "plot, x, y",
    ]
    assert main(argv) == 0

def ttest_numpy_data():
    argv = [
        "-x", "numpy.arange(3)",
        "-y", "numpy.random~rand(3)",
        "-t", "'test', fontsize=24",
        "--xlabel", "'xlabel'",
        "--xticks", "x, ['a', 'b', 'c']",
        "--ylabel", "'ylabel'",
        "-p", "scatter, x, y, label='s'",
        "-p", "scatter, y, x, label='t'",
        "-l",
    ]
    assert main(argv) == 0

def ttest_numpy_text():
    argv = [
        "%s"%numpy_text_data1,
        "-x", "d0[1,:]",
        "-p", "plot, x**2",
    ]
        #"--data-format", "numpytext, delimiter=','",
    assert main(argv) == 0

def test_csv_file():
    argv = [
        "%s"%csv_text_data1,
        "-x", "d0[1,:]",
        "-y", "x.astype(numpy.float)",
        "-z", "max(d0[1,:])",
        "-p", "plot, y**2",
        "--data-format", "csv, delimiter=';'",
        #"--calc", "y = y**2",
        #"--printvar", "x",
        #"--pages", "2, pdf_merge=true",
        #"--noplot",
        "--save", "'test.pdf'",

    ]
    assert main(argv) == 0
