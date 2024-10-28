# -*- coding: utf-8 -*-

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

