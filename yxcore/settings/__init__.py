# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
import types
from functools import reduce
from yxcore.utility import const
from yxcore.utility.loader import safe_method_call
from yxcore import event
from yxcore import environment as env


__author__ = 'yuxi'


"""
配置优先级
动态配置 > 全局配置 > 默认配置


动态配置:
程序运行中，可以实时设定的配置项
使用regist函数这顶

全局配置
指定的全局配置文件设定的配置
在sys.modules[SETTING_KEY.CUSTOM_SETTING_MODUE_NAME]中。外层必须使用category字典包裹

默认配置
每个模块设定的默认配置
使用regist_default函数设定

"""


"""
一些配置项的key
"""
SETTING_KEY = const.YXConstGenerator()

# 使用这个key 从environment 中取出配置文件的名字
SETTING_KEY.ENVIRONMENT_SETTING_KEY = 'YXCORE_SETTING_MODULE'
# 使用这个key 从sys.module 中取出setting module
SETTING_KEY.CUSTOM_SETTING_MODUE_NAME = 'YXCORE_CUSTOM_SETTING_MODULE'

# 是否是调试模式
SETTING_KEY.DEBUG_MODE = 'DEBUG'

# 安装的python lib
SETTING_KEY.INSTALLED_LIBS = 'YXINSTALLED_LIBS'

# yxcore 的路径
SETTING_KEY.YXCORE_PATH = 'YXCORE_PATH'


"""
事件
"""
SETTING_EVENT = const.YXConstGenerator()
# 事件，配置文件加载完毕, 所有其他操作必须在这个事件之后做
SETTING_EVENT.SETTINGS_LOAD_FINISHED = 'EVENT_SETTING_LOAD_FINISHED'


"""
默认配置
"""
default_setting = {}

"""
动态配置
"""
dynamic_setting = {}


def _keypath_walker_generator(module):
    """
    创建一个reduce的回掉
    """

    def _keypath_walker(key1, key2):

        if isinstance(key1, str):
            value = _value_for_object(module, key1)
        else:
            value = key1

        if value is not None:
            value = _value_for_object(value, key2)

        return value

    return _keypath_walker


def _value_for_object(unknown_object, key_path):
    """
    判断unknown_object类型, 根据类型使用key取出对应的值
    """

    key_list = key_path.split('.')

    if len(key_list) is 1:

        if isinstance(unknown_object, types.ModuleType):
            return getattr(unknown_object, key_path, None)
        elif isinstance(unknown_object, dict):
            return unknown_object.get(key_path, None)
        else:
            return None

    else:
        return reduce(_keypath_walker_generator(unknown_object), key_list)


def regist_default(category, key, value):
    config = default_setting.setdefault(category if category is not None else '', {})
    config[key] = value


def regist(category, key, value):
    config = dynamic_setting.setdefault(category if category is not None else '', {})
    config[key] = value


def setting_for_keypath(key_path):

    dynamic_value = _value_for_object(dynamic_setting, key_path)

    custom_value = None
    if SETTING_KEY.CUSTOM_SETTING_MODUE_NAME in sys.modules:
        custom_value = _value_for_object(sys.modules[SETTING_KEY.CUSTOM_SETTING_MODUE_NAME], key_path)

    default_value = _value_for_object(default_setting, key_path)

    value = None
    if dynamic_value is not None:
        value = dynamic_value

        # 如果value 是字典，试着合并 custom 和 默认参数
        if isinstance(value, dict):

            # 将value并入customValue
            if isinstance(custom_value, dict):
                value = {**custom_value, **value}

            # 如果value 是字典，试着合并 default value
            if isinstance(default_value, dict):
                value = {**default_value, **value}

    elif custom_value is not None:
        value = custom_value

        # 如果value 是字典，试着合并 default value
        if isinstance(default_value, dict):
            if isinstance(default_value, dict):
                value = {**default_value, **value}

    elif default_value is not None:
        value = default_value

    # 尝试对value进行一份设置的拷贝，防止污染
    copyed_value = safe_method_call(value, 'copy')

    return copyed_value if copyed_value is not None else value


def default_setting_for_key_path(key_path):
    pass


def path_join(*args):
    return '.'.join(args)


# 标记是否初始化完毕
_finish_loading = False


def load_finished():
    global _finish_loading

    if _finish_loading is False:
        _finish_loading = True
        event.send(SETTING_EVENT.SETTINGS_LOAD_FINISHED)


def is_load_finished():
    return _finish_loading
