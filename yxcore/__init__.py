# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function
import os

__author__ = 'yuxi'

os.environ.setdefault('YXCORE_PATH', os.path.dirname(__file__))

try:
    import six
except ImportError as e:
    from .utility import loader
    import sys

    print('error: 无法找到six模块，尝试使用自带机制', file=sys.stdout)
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vendors/six')
    loader.load(path)

try:
    import backports.inspect
except ImportError as e:
    from .utility import loader
    import sys

    print('error: 无法找到backports.inspect模块，尝试使用自带机制', file=sys.stdout)
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vendors/backports.inspect')
    module = loader.load(path)
