# -*- coding: utf-8 -*-

from __future__ import unicode_literals

__author__ = 'yuxi'


class YXCoreException(Exception):
    pass


class YXLauchErrorException(YXCoreException):
    pass


class YXTypeErrorException(TypeError):
    pass


class YXParameterErrorException(TypeError):
    pass


class YXSettingErrorException(TypeError):
    pass

