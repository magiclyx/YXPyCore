# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import sys
from yxcore.utility.exception import YXTypeErrorException

__author__ = 'yuxi'


class YXConstGenerator(object):
    class YXConstErrorException(YXTypeErrorException):
        pass

    def _setattr__(self, key, value):
        if key in self.__dict__:
            raise self.YXConstErrorException("constant reassignment error!")
        self.__dict__[key] = value

sys.modules['const'] = YXConstGenerator()


