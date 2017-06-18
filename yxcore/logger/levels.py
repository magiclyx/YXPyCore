# -*- coding: utf-8 -*-


"""
这里包装了python 的 logging。如果要自己实现，注意看一下logging的实现
"""

from __future__ import unicode_literals

import logging

__author__ = 'yuxi'


"""日志level"""
CRITICAL = logging.CRITICAL
FATAL = logging.FATAL
ERROR = logging.ERROR
WARNING = logging.WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTICE = DEBUG - 1
TRACE = NOTICE - 1
NOTSET = logging.NOTSET


def get_level_name(level):
    logging.getLevelName(level)


def add_level_name(level, level_name):
    logging.addLevelName(level, level_name)
