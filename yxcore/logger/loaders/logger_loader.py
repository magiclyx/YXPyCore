# -*- coding: utf-8 -*-

from yxcore.logger.loaders import common
from yxcore.logger.loaders import handler_loader
from yxcore.logger.loaders.common import LOGGER_KEY
from yxcore.utility.exception import YXSettingErrorException, YXLauchErrorException
import logging


class LoggerLoader(common.BasicLoader):

    cached_logger = {}

    def __init__(self, name):
        super(LoggerLoader, self).__init__(name)
        self.name = name

        self.level = self.value_for_key('level')
        if self.level is None:
            self.level = self.default_value_for_key(LOGGER_KEY.DEFAULT_LOG_LEVEL)

        self.propagate = self.value_for_key('propagate')
        if self.propagate is None:
            self.propagate = self.default_value_for_key(LOGGER_KEY.DEFAULT_LOG_PROPAGATE)

        self.handlers_name_list = self.value_for_key('handlers')
        if self.handlers_name_list is None:
            self.handlers_name_list = self.default_value_for_key(LOGGER_KEY.DEFAULT_LOG_HANDLE)

    def load(self):
        # 初始化 handle
        logger = logging.getLogger(self.name)

        # 设置level
        if self.level is not None:
            logger.setLevel(self.level)

        # 设置propagate
        if self.propagate is not None:
            logger.propagate = self.propagate

        # 设置hander
        for handler_name in self.handlers_name_list:
            hander_loader = handler_loader.loader_for_key(handler_name)
            if hander_loader is None:
                raise(YXSettingErrorException, '未找到日志Hander:%s' % (handler_name, ))

            hander = hander_loader.load()
            if hander is None:
                raise (YXSettingErrorException, '不能从日志loader加载Hander:%s' % (handler_name,))

            logger.addHandler(hander)

        return logger

    @classmethod
    def key(cls):
        return LOGGER_KEY.LOGGERS


_cached_loaders = None


def initialize():
    global _cached_loaders

    if _cached_loaders is None:
        _cached_loaders = dict()

        all_config = common.value_for_path(LoggerLoader.key())
        if all_config is None:
            all_config = dict()

        for name in all_config:
            _cached_loaders[name] = LoggerLoader(name)


def has_initialize():
    return True if _cached_loaders is not None else False


def get_loaders():
    if _cached_loaders is None:
        raise YXLauchErrorException('日志模块初始化之前，尝试获取logger')

    return _cached_loaders


def loader_for_key(key):
    return get_loaders().get(key, None)
