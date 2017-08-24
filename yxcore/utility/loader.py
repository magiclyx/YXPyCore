# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
import os
import importlib


__author__ = 'yuxi'


def load(path, **kwargs):
    """
    加载库，支持参数
    module_name 额外置顶一个模块名称
    force_reload 若模块已经加载，是否强制重新加载
    """

    # 取kwargs 参数
    module_name = kwargs.get('module_name', None)
    forece_reload = kwargs.get('forece_reload', False)

    def _py2_check_magic_num(cache_path):
        """
        验证编译后文件的magic number , 是否和当前python解释器兼容
        """
        import imp
        if os.access(cache_path, os.F_OK) and os.access(cache_path, os.R_OK):
            with open(cache_path, 'r') as f:
                magic = f.read(4)
                if magic is not None:
                    return True if magic == imp.get_magic() else False

    def _fixed_cache_from_source(source_path):
        """
        根据python文件，获取编译后缓存文件的位置

        注意：！！！！
        这里貌似有问题。已经发现了代码改动后还是执行以前cache的情况。
        试着把cache删掉，看看会不会解决问题！！！！！
        """

        if sys.version_info[0] is 2:
            import imp
            cache_path = source_path + '.pyc'
            if _py2_check_magic_num(cache_path) is True:
                return cache_path

            cache_path = source_path + '.pyo'
            if _py2_check_magic_num(cache_path) is True:
                return cache_path

            return None
        elif sys.version_info[0] is 3:
            import importlib.util
            # 实际上，cache_from_source 是需要.py扩展名的, 上面是为了处理方便. 这部分可以考虑重写
            return importlib.util.cache_from_source(source_path + '.py')
        else:
            raise ImportError('not implement in python %d.%d.%d' % sys.version_info[0:3])

    def _fixed_load_compiled(load_module_name, load_module_path):
        """
        加载编译后的文件
        """
        if forece_reload is False and load_module_name in sys.modules:
            return sys.modules[load_module_name]

        if sys.version_info[0] == 2:
            import imp
            return imp.load_compiled(load_module_name, load_module_path)
        elif sys.version_info[0] is 3:
            import importlib
            if sys.version_info[0:2] > (3, 4):
                import importlib.util
                spec = importlib.util.spec_from_file_location(load_module_name, load_module_path)
                result_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(result_module)
                sys.modules[load_module_name] = result_module
                return result_module
            else:
                import importlib.machinery
                return importlib.machinery.SourcelessFileLoader(load_module_name, load_module_path).load_module()

    def _fixed_load_normal(load_module_name, load_module_path):
        """
        加载源码文件
        """
        if forece_reload is False and load_module_name in sys.modules:
            return sys.modules[load_module_name]

        if sys.version_info[0] == 2:
            import imp
            return imp.load_source(load_module_name, load_module_path)
        elif sys.version_info[0] is 3:
            if sys.version_info[0:2] > (3, 4):
                import importlib.util
                spec = importlib.util.spec_from_file_location(load_module_name, load_module_path)
                result_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(result_module)
                sys.modules[load_module_name] = result_module
                return result_module
            else:
                import importlib.machinery
                return importlib.machinery.SourceFileLoader(load_module_name, load_module_path).load_module()

    def _try_load_with_no_ext_path(try_module_name, try_path):
        """
        尝试加载已经去除扩展名的python模块
        """

        result_module = None

        guess_path = _fixed_cache_from_source(try_path)
        if guess_path is not None and os.access(guess_path, os.F_OK) and os.access(guess_path, os.R_OK):
            result_module = _fixed_load_compiled(try_module_name, guess_path)

        guess_path = try_path + '.py'
        if guess_path is not None and result_module is None and os.access(guess_path, os.F_OK) and os.access(guess_path, os.R_OK):
            result_module = _fixed_load_normal(try_module_name, guess_path)

        return result_module

    # 去除扩展名
    no_ext_path = path
    if path.endswith('.py') or path.endswith('.pyc'):
        no_ext_path, _ = os.path.splitext(path)

    # 获得父文件夹 以及 包信息
    parent_path, package_info = os.path.split(no_ext_path)

    # 访问沿途的所有包(访问包的 __init__)
    package_path = parent_path
    current_package_info = None
    package_list = package_info.split('.')
    module = None
    for package_name in package_list:

        if current_package_info is None:
            current_package_info = package_name
        else:
            current_package_info = '.'.join([current_package_info, package_name])

        package_path = os.path.join(package_path, package_name)
        module = _try_load_with_no_ext_path(current_package_info, package_path)
        if module is None:
            module = _try_load_with_no_ext_path(current_package_info, os.path.join(package_path, '__init__'))

        if module is None:
            raise ImportError('无效包路径 %s' % (path, ))

    if module is not None and module_name is not None:
        if module_name not in sys.modules:
            sys.modules[module_name] = module

    return module


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
    #module = sys.modules.get(module_name, None)
    module = load(module_name)
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
