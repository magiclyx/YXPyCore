# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging
import logging.handlers

from yxcore.logger.loaders import common
from yxcore.utility import loader
from yxcore.logger.loaders import formatter_loader
from yxcore.logger.loaders import filter_loader
from yxcore.logger.loaders.common import LOGGER_KEY
from yxcore.utility.exception import YXSettingErrorException


__author__ = 'yuxi'


class HandlerLoader(common.BasicLoader):

    def __init__(self, name):
        super(HandlerLoader, self).__init__(name)
        self.level = self.value_for_key('level')
        self.formatter_name = self.value_for_key('formatter')

        self.filter_list = self.value_for_key('filters')
        if self.filter_list is None:
            self.filter_list = []

    # 这个函数用于向已有的handlers设置 level, formatter, filter.
    # 实际上是个私有函数
    def setup_handler(self, handle):
        # 设置level
        if self.level is not None:
            handle.setLevel(self.level)

        # 设置Formatter
        if self.formatter_name is not None:
            log_formatter_loader = formatter_loader.loader_for_key(self.formatter_name)
            if log_formatter_loader is None:
                raise YXSettingErrorException('未找到日志Formatter:%s' % (self.formatter_name, ))

            log_formatter = log_formatter_loader.load()
            if log_formatter is None:
                raise YXSettingErrorException('不能从日志loader加载Formatter:%s' % (self.formatter_name, ))

            handle.setFormatter(log_formatter)

        # 设置Filter
        for filter_name in self.filter_list:
            log_filter_loader = filter_loader.loader_for_key(filter_name)
            if log_filter_loader is None:
                raise YXSettingErrorException('未找到日志filter:%s' % (filter_name,))

            log_filter = log_filter_loader.load()
            if log_filter is None:
                raise YXSettingErrorException('不能从日志loader加载Filter:%s' % (filter_name,))

            handle.addFilter(log_filter)

        return handle

    @classmethod
    def key(cls):
        return LOGGER_KEY.HANDLERS

    def load(self):
        return None


_cached_loaders = None


def get_loaders():

    global _cached_loaders

    if _cached_loaders is None:

        _cached_loaders = dict()

        all_config = common.value_for_path(HandlerLoader.key())
        if all_config is None:
            all_config = dict()

        for name in all_config:
            class_path = all_config[name].get('loader', None)
            if class_path is None:
                raise ImportError('日志handler:%s没有配置class属性' % (name,))
            _cached_loaders[name] = loader.item_by_path(class_path)(name)

    return _cached_loaders


def loader_for_key(key):
    return get_loaders().get(key, None)


class NullHandlerLoader(HandlerLoader):
    def load(self):
        return logging.NullHandler()


class StreamHandlerLoader(HandlerLoader):

    def __init__(self, name):
        super(StreamHandlerLoader, self).__init__(name)
        self.stream = None  # 这个使用默认的None, 方便子类继承。

        # 这个不应该付值，应该在子类中直接定义
        # self.stream = self.value_for_key('stream')

    def load(self):
        return logging.StreamHandler(self.stream)


class FileHandlerLoader(HandlerLoader):

    def __init__(self, name):
        super(FileHandlerLoader, self).__init__(name)
        self.filename = self.value_for_key('file')
        self.encoding = self.value_for_key('encoding')

        self.delay = self.value_for_key('delay')
        if self.delay is None:
            self.delay = False

        self.mode = self.value_for_key('mode')
        if self.mode is None:
            self.mode = 'a'  # 这里 mode 使用默认值

    def load(self):
        # 初始化 handle
        handle = logging.FileHandler(self.filename, self.mode, self.encoding, self.delay)
        return self.setup_handler(handle)


class WatchedFilHandlerLoader(FileHandlerLoader):
    """不需要实例话，是基类"""


class BaseRotatingHandlerLoader(FileHandlerLoader):
    pass


class RotatingFileHandlerLoader(BaseRotatingHandlerLoader):

    def __init__(self, name):
        super(RotatingFileHandlerLoader, self).__init__(name)

        max_bytes_string = self.value_for_key('maxBytes')
        self.maxBytes = int(max_bytes_string) if max_bytes_string is not None else 0

        buckup_count_string = self.value_for_key('backupCount')
        self.buckupCount = int(buckup_count_string) if buckup_count_string is not None else 0

    def load(self):
        handle = logging.handlers.RotatingFileHandler(self.filename, self.mode, self.maxBytes, self.buckupCount, self.encoding, self.delay)
        return self.setup_handler(handle)


class TimedRotatingFileHandlerLoader(BaseRotatingHandlerLoader):

    def __init__(self, name):
        super(TimedRotatingFileHandlerLoader, self).__init__(name)
        self.when = self.value_for_key('when')
        if self.when is None:
            self.when = 'h'

        interval_string = self.value_for_key('interval')
        self.interval = int(interval_string) if interval_string is not None else 1

        buckup_count_string = self.value_for_key('backupCount')
        self.buckupCount = int(buckup_count_string) if buckup_count_string is not None else 0

        self.utc = self.value_for_key('utc')
        if self.utc is None:
            self.utc = False

        self.atTime = self.value_for_key('atTime')

    def load(self):
        handle = logging.handlers.TimedRotatingFileHandler(self.filename, self.when, self.interval, self.buckupCount, self.encoding, self.delay, self.utc, self.atTime)
        return self.setup_handler(handle)
