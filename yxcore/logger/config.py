# -*- coding: utf-8 -*-


"""
这里包装了python 的 logging。如果要自己实现，注意看一下logging的实现
"""

from __future__ import unicode_literals


__author__ = 'yuxi'


# 输出格式
formatters = {
    'verbose': {
        'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        'datefmt': '%a, %d %b %Y %H:%M:%S',
    },
    'simple': {
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
# Todo 提供常用Handle的默认配置
handlers = {
    'null': {
        'loader': 'yxcore.logger.loaders.handler_loader.NullHandlerLoader',
        'level': 'DEBUG',
        'formatters': 'simple',
        'filters': [],
    },
    'stream': {
        'loader': 'yxcore.logger.loaders.handler_loader.StreamHandlerLoader',
        'level': 'DEBUG',
        'formatter': 'simple',
        'filters': [],
    },
    'file': {
        'loader': 'yxcore.logger.loaders.handler_loader.FileHandlerLoader',
        'level': 'ERROR',
        'formatter': 'simple',
        'filters': [],
        'file': None,
    },
    'watched_file': {
        'loader': 'yxcore.logger.loaders.handler_loader.WatchedFilHandlerLoader',
        'level': 'ERROR',
        'formatters': 'simple',
        'filters': [],
        'file': None,
    },
    'rotating_file': {
        'loader': 'yxcore.logger.loaders.handler_loader.RotatingFileHandlerLoader',
        'level': 'ERROR',
        'formatters': 'simple',
        'filters': [],
        'file': None,
        'maxBytes': None,
        'buckupCount': None,
    },
    'time_rotating_file': {
        'loader': 'yxcore.logger.loaders.handler_loader.TimedRotatingFileHandlerLoader',
        'level': 'ERROR',
        'formatters': 'simple',
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

# 日志
loggers = {
    'com.yxcore.logger': {
        'handlers': ['null'],
        'propagate': True,
        'level': 'INFO',
    },
    'django.request': {
        'handlers': ['mail_admins'],
        'level': 'ERROR',
        'propagate': False,
    },
    'myproject.custom': {
        'handlers': ['console', 'mail_admins'],
        'level': 'INFO',
        # 'filters': ['special']
    }
}
