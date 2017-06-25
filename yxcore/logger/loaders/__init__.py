# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import logging
from yxcore.logger import config
from yxcore import settings
from yxcore.logger import levels
from yxcore.logger.loaders import common
from yxcore.logger.loaders.common import LOGGER_KEY
from yxcore.logger.loaders import logger_loader
from yxcore.utility.exception import YXLauchErrorException


__author__ = 'yuxi'


""" 设置默认配置 """
# 日志格式
settings.regist_default(LOGGER_KEY.CATEGORY_NAME, LOGGER_KEY.FORMATTERS, config.formatters)
# 过滤器
settings.regist_default(LOGGER_KEY.CATEGORY_NAME, LOGGER_KEY.FILTERS, config.filters)
# handlers
settings.regist_default(LOGGER_KEY.CATEGORY_NAME, LOGGER_KEY.HANDLERS, config.handlers)
# 日志


settings.regist_default(LOGGER_KEY.CATEGORY_NAME, LOGGER_KEY.LOGGERS, config.loggers)
# 默认日志 - id
settings.regist_default(LOGGER_KEY.CATEGORY_NAME, LOGGER_KEY.DEFAULT_LOG_IDENTIFIER, config.default_log_identifier)
# 默认 - handlers
settings.regist_default(LOGGER_KEY.CATEGORY_NAME, LOGGER_KEY.DEFAULT_LOG_HANDLE, config.default_log_handle)
# 默认 - level
settings.regist_default(LOGGER_KEY.CATEGORY_NAME, LOGGER_KEY.DEFAULT_LOG_LEVEL, config.default_log_level)
# 默认 - formatters
settings.regist_default(LOGGER_KEY.CATEGORY_NAME, LOGGER_KEY.DEFAULT_LOG_FORMATTER, config.default_log_formatters)
# 默认 - filters
settings.regist_default(LOGGER_KEY.CATEGORY_NAME, LOGGER_KEY.DEFAULT_LOG_FILTER, config.default_log_filters)
# 默认 - propagate
settings.regist_default(LOGGER_KEY.CATEGORY_NAME, LOGGER_KEY.DEFAULT_LOG_PROPAGATE, config.default_log_propagate)


_default_logger_identifier = None
_cached_logger = {}


def initialize():
    global _default_logger_identifier

    # 添加notice 和 trace 日志级别
    logging.addLevelName(levels.NOTICE, 'NOTICE')
    logging.addLevelName(levels.TRACE, 'TRACE')

    # 初始化 默认 logger 的 id
    if _default_logger_identifier is None:
        _default_logger_identifier = common.value_for_path(LOGGER_KEY.DEFAULT_LOG_IDENTIFIER)

    # 初始化loader
    logger_loader.initialize()


def get_logger(identifier=None):

    global _default_logger_identifier
    global _cached_logger

    if _default_logger_identifier is None:
        raise YXLauchErrorException('日志模块初始化之前，尝试获取logger')

    # 如果identifier 取默认identifier
    if identifier is None:
        identifier = _default_logger_identifier

    if identifier in _cached_logger:
        return _cached_logger.get(identifier)
    else:
        # 获取logger 的 loader
        loader = logger_loader.loader_for_key(identifier)

        # 返回 logger( 如果上一部取loader失败，则使用 logging.getLogger 直接返回一个logger)
        if loader is not None:
            logger = loader.load()
            _cached_logger[identifier] = logger  # 只有从loader加载的，才使用cache. 这给identifier重新申请的机会
        else:
            logger = logging.getLogger(identifier)

        return logger


def get_default_logger():
    return get_logger()
