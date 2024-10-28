# -*- coding: utf-8 -*-

from yxcore.logger.loaders import common
from yxcore.logger.loaders.common import LOGGER_KEY

__author__ = 'yuxi'


class FilterLoader(common.BasicLoader):
    """
    暂时未支持，实现参考handler
    """

    def __init__(self, name):
        super(FilterLoader, self).__init__(name)

    def load(self):
        return None

    @classmethod
    def key(cls):
        return LOGGER_KEY.FILTERS


def get_loaders():
    return None


def loader_for_key(key):
    return None
