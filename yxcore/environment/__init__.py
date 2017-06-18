# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys

__author__ = 'yuxi'


def is_python3():
    """
    用于显示的判断是否是python3版本，今后可以去掉对python2的支持

    注意，同时搜索 "#:~ python2 adaptation" 注释，用于 python2 不支持的语法
    """
    return True if sys.version_info[0] >= 3 else False
