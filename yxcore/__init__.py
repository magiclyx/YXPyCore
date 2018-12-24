# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function
import os
import sys

__author__ = 'yuxi'

YXCORE_PACKAGE_PATH = os.path.dirname(__file__)

os.environ.setdefault('YXCORE_PATH', YXCORE_PACKAGE_PATH)
sys.path.append(os.path.join(YXCORE_PACKAGE_PATH, 'vendors'))

