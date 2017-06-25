# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import logging
from yxcore.logger.loaders import common
from yxcore.logger.loaders.common import LOGGER_KEY


__author__ = 'yuxi'


class FormatterLoader(common.BasicLoader):

    def __init__(self, name):
        super(FormatterLoader, self).__init__(name)
        self.format = self.value_for_key('format')
        self.datefmt = self.value_for_key('datefmt')

    def load(self):
        return logging.Formatter(self.format, self.datefmt)

    @classmethod
    def key(cls):
        return LOGGER_KEY.FORMATTERS


"""保存的，已经从配置文件中加载的loaders"""
_cached_loaders = None


def get_loaders():

    global _cached_loaders

    if _cached_loaders is None:
        _cached_loaders = dict()

        all_config = common.value_for_path(FormatterLoader.key())
        if all_config is None:
            all_config = dict()

        for name in all_config:
            _cached_loaders[name] = FormatterLoader(name)

    return _cached_loaders


def loader_for_key(key):
    return get_loaders().get(key, None)
