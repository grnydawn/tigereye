#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `tigereye` package."""

import sys
import pytest

from tigereye import main

def ttest_main():
    assert main(["[1,2,3]"]) == 0


def ttest_data_in_cmdline():
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

def test_numpy_data():
    argv = [
        "-x", "numpy.arange(3).random~shuffle(x)",
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
