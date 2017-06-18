# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from yxcore.utility import const
from yxcore import settings
# from yxcore.logger.loaders import common


__author__ = 'yuxi'


"""logger 常量"""
LOGGER_KEY = const.YXConstGenerator()
LOGGER_KEY.CATEGORY_NAME = 'YXLOGGER'
LOGGER_KEY.DEFAULT_LOG_IDENTIFIER = 'default_log_identifier'
LOGGER_KEY.FORMATTERS = 'formatters'
LOGGER_KEY.FILTERS = 'filters'
LOGGER_KEY.HANDLERS = 'handlers'
LOGGER_KEY.LOGGERS = 'loggers'


def value_for_path(*args):
    """用于获取YXLogger下的配置项"""
    return settings.setting_for_keypath(settings.path_join(LOGGER_KEY.CATEGORY_NAME, *args))


class BasicLoader(object):

    def __init__(self, name):
        self.name = name

    def value_for_key(self, key):
        """用于获取YXLogger.xxx 的配置项(xxx 由name指定) """
        # return common.value_for_path(self.__class__.key(), self.name, key)
        return value_for_path(self.__class__.key(), self.name, key)

    def load(self):
        return None

    @classmethod
    def key(cls):
        return None

