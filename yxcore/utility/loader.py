# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
import importlib


__author__ = 'yuxi'


# module_name 指定加载后的名字。如果未指定，则使用path作为module_name
def load(path, module_name=None):
    lib = importlib.import_module(path)
    sys.modules[module_name if module_name is not None else path] = lib
    return lib


def module_by_path(path):
    return importlib.import_module(path)


def item_by_path(path):
    """
    使用一个path, 获取一个obj

    :param path:  e.g call this function use : item_by_path('yxcore.utility.loader.item_by_path')(path)
    """

    index = path.rfind('.')
    if index < 0 or index >= len(path) - 1:
        raise ImportError('错误的lib名称:%s' % (path,))

    module_name = path[:index]
    class_name = path[index + 1:]

    # module 必须已经加载, build-in module, 已经import, 使用importlib.import_module 加载
    module = sys.modules.get(module_name, None)
    if module is None:
        raise ImportError('没有找到module:%s' % (module_name,))

    return getattr(module, class_name, None)


def obj_has_attr(obj, attr_name):
    """
    判断某个obj是否包含一个属性

    :param obj: obj
    :param attr_name: 属性的名字(字符串)
    :return:
    """
    invert_op = getattr(obj, attr_name, None)
    if callable(invert_op):
        return True
    else:
        return False


def safe_method_call(obj, method_name, *argv, **kwargs):
    """
    如果一个obj中包含method_name方法，则调用这个方法，否则什么也不做

    :param obj:
    :param method_name: 方法的名字
    :param argv: 方法的参数
    :param kwargs:  方法的参数
    :return:
    """
    invert_op = getattr(obj, method_name, None)
    if callable(invert_op):
        return invert_op(*argv, **kwargs)

    return None
