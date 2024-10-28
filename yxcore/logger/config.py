# -*- coding: utf-8 -*-


"""
这里包装了python 的 logging。如果要自己实现，注意看一下logging的实现
"""


__author__ = 'yuxi'


# 输出格式
formatters = {
    'verbose': {
        'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        'datefmt': '%a, %d %b %Y %H:%M:%S',
    },
    'raw': {
        'format': '%(levelname)s %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S',
    },
}

# 过滤器，暂时不支持
filters = {
    # 'special': {
    #      '()': 'project.logging.SpecialFilter',
    #      'foo': 'bar',
    # },
}

# handlers
# handle 的 level 默认为NOTSET。 这样可以使用logger的配置
# Todo 提供常用Handle的默认配置
handlers = {
    'null': {
        'loader': 'yxcore.logger.loaders.handler_loader.NullHandlerLoader',
        'level': 'NOTSET',
        'formatter': 'raw',
        'filters': [],
    },
    'stream': {
        'loader': 'yxcore.logger.loaders.handler_loader.StreamHandlerLoader',
        'level': 'NOTSET',
        'formatter': 'raw',
        'filters': [],
    },
    #  TODO 这个console 是因为 stream 功能不全
    'console': {
        'loader': 'yxcore.logger.loaders.handler_loader.StreamHandlerLoader',
        'level': 'NOTSET',
        'formatter': 'raw',
        'filters': [],
    },
    'file': {
        'loader': 'yxcore.logger.loaders.handler_loader.FileHandlerLoader',
        'level': 'NOTSET',
        'formatter': 'raw',
        'filters': [],
        'file': None,
    },
    'watched_file': {
        'loader': 'yxcore.logger.loaders.handler_loader.WatchedFilHandlerLoader',
        'level': 'NOTSET',
        'formatter': 'raw',
        'filters': [],
        'file': None,
    },
    'rotating_file': {
        'loader': 'yxcore.logger.loaders.handler_loader.RotatingFileHandlerLoader',
        'level': 'NOTSET',
        'formatter': 'raw',
        'filters': [],
        'file': None,
        'maxBytes': None,
        'buckupCount': None,
    },
    'time_rotating_file': {
        'loader': 'yxcore.logger.loaders.handler_loader.TimedRotatingFileHandlerLoader',
        'level': 'NOTSET',
        'formatter': 'raw',
        'filters': [],
        'file': None,
        'when': None,
        'interval': None,
        'buckupCount': None,
        'utc': None,
        'atTime': None,
    },


}

# 默认日志 identifier
default_log_identifier = 'com.yxcore.logger'
default_log_handle = ['console', ]
default_log_formatters = 'raw'
default_log_level = 'DEBUG'
default_log_filters = []
default_log_propagate = True

# 日志
loggers = {
    'com.yxcore.logger': {
        'handlers': ['console'],
        'propagate': True,
        'level': 'INFO',
    },
}
