# -*- coding: utf-8 -*-


"""
这里包装了python 的 logging。如果要自己实现，注意看一下logging的实现
"""

from __future__ import unicode_literals
import sys
import inspect
import os
from yxcore import event
from yxcore import environment as env
from yxcore.settings import SETTING_EVENT
from yxcore.logger import loaders
from yxcore.logger import levels


__author__ = 'yuxi'


class Std(object):
    """
    标准输出的logger
    """
    @staticmethod
    def output(*args, **kwargs):
        print(*args, file=sys.stdout, **kwargs)

    @staticmethod
    def error(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)


class Logger(object):
    """
    YXLogger
    级别:CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTICE > TRACE >NOTSET
    默认情况下:级别为WARNING
    """

    def __init__(self, identifier=None):
        self.logger = loaders.get_logger(identifier)

    def set_level(self, level):
        self.logger.setLevel(level)

    def is_enable_for(self, level):
        return self.logger.isEnabledFor(level)

    def log(self, level, msg, *args, **kwargs):
        self.logger.log(level, msg, *args, **kwargs)

    def trace(self, msg, *args, **kwargs):
        self.log(levels.TRACE, msg, *args, **kwargs)

    def notice(self, msg, *args, **kwargs):
        self.log(levels.NOTICE, msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        self.logger.exception(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)


"""
默认日志模块
"""
_default = None


# 响应配置文件加载完毕事件
@event.event_handle(SETTING_EVENT.SETTINGS_LOAD_FINISHED)
def setting_load_finish_event_handle(event):
    global _default

    # 初始化loader
    loaders.initialize()

    # 取默认logger(identifier=None)
    _default = Logger()


def log(level, msg, *args, **kwargs):
    _default.log(level, msg, *args, **kwargs)


def trace(msg, *args, **kwargs):
    _default.trace(msg, *args, **kwargs)


def notice(msg, *args, **kwargs):
    _default.notice(msg, *args, **kwargs)


def debug(msg, *args, **kwargs):
    _default.debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    _default.info(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    _default.warning(msg, *args, **kwargs)


def exception(msg, *args, **kwargs):
    _default.exception(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    _default.error(msg, *args, **kwargs)


def critical(msg, *args, **kwargs):
    _default.critical(msg, *args, **kwargs)


def get_logger(identifier=None):
    if identifier is not None:
        return Logger(identifier)
    else:
        return _default


# # TRACE_5 = NOTICE - 1     #函数名
# # TRACE_4 = TRACE_5 - 1    #详细函数名
# # TRACE_3 = TRACE_4 - 1    #详细函数名，参数
# # TRACE_2 = TRACE_3 - 1    #详细函数名，参数，返回值
# # TRACE_1 = TRACE_2 - 1    #详细函数名，参数，返回值，local信息
# # TRACE_0 = TRACE_1 - 1    #全局trace
#
# def _trace_info(trace_num, return_value, *args, **kwargs):
#
#     frame = inspect.stack()[2].frame
#
#     if trace_num is 5:
#         return '[** %s **]' % (frame.f_code.co_name, )
#     elif trace_num is 4:
#         return '[** %s:%s:%d **]' % (os.path.basename(frame.f_code.co_filename), frame.f_code.co_name, frame.f_lineno)
#     elif trace_num is 3:
#         return '[** %s:%s:%d(%r, %r)->%r **]' % (os.path.basename(frame.f_code.co_filename), frame.f_code.co_name, frame.f_lineno, args, kwargs, return_value)
#     elif trace_num is 2:
#         return '[** %s:%s:%d(%r, %r){%r}->%r **]' % (os.path.basename(frame.f_code.co_filename), frame.f_code.co_name, frame.f_lineno, args, kwargs, frame.f_locals, return_value)
#     else:
#         raise ""
#
#
# def tracefun(trace_level=4):
#     def _trace(fun):
#         def _decorated(*args, **kwargs):
#             if _default.is_enable_for(levels.TRACE):
#
#                 try:
#                     result = fun(*args, **kwargs)
#                     trace(_trace_info(trace_level, result, *args, **kwargs))
#                     return result
#                 except Exception as e:
#                     trace(_trace_info(trace_level, 'crashed', *args, **kwargs))
#                     raise e
#             else:
#                 return fun(*args, **kwargs)
#
#         return _decorated
#
#     return _trace



