# -*- coding: utf-8 -*-
"""tigereye main module."""

class Error(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class InternalError(Error):
    pass

class UsageError(Error):
    pass

class NormalExit(Error):
    pass

