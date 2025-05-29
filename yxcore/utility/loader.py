# -*- coding: utf-8 -*-

import sys
import os
import importlib


__author__ = 'yuxi'


def load(path, **kwargs):
    """
    加载库，支持参数
    module_name 额外置顶一个模块名称
    force_reload 若模块已经加载，是否强制重新加载
    force_cache 优先使用缓存(注意这里有问题，如果强制使用缓存。如果代码改变了，但还是会运行之前缓存的逻辑)
    """

    # 取kwargs 参数
    module_name = kwargs.get('module_name', None)
    force_reload = kwargs.get('force_reload', False)
    force_cache = kwargs.get('force_cache', False)

    def _fixed_cache_from_source(source_path):
        """
        这里需要找一个方法，判断文件是否被改变了。
        """
        if force_cache:
            import importlib.util
            # 实际上，cache_from_source 是需要.py扩展名的, 上面是为了处理方便. 这部分可以考虑重写
            return importlib.util.cache_from_source(source_path + '.py')
        else:
            return None


    def _fixed_load_compiled(load_module_name, load_module_path):
        """
        加载编译后的文件
        """
        if force_reload is False and load_module_name in sys.modules:
            return sys.modules[load_module_name]

        if sys.version_info[0] == 2:
            import imp
            return imp.load_compiled(load_module_name, load_module_path)
        elif sys.version_info[0] == 3:
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
        if force_reload is False and load_module_name in sys.modules:
            return sys.modules[load_module_name]

        if sys.version_info[0] == 2:
            import imp
            return imp.load_source(load_module_name, load_module_path)
        elif sys.version_info[0] == 3:
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

    from yxcore.settings import SETTING_KEY

    index = path.rfind('.')
    if index < 0 or index >= len(path) - 1:
        raise ImportError('错误的lib名称:%s' % (path,))

    module_name = path[:index]
    class_name = path[index + 1:]

    # 尝试从已加载的模块中获取
    # module 必须已经加载, build-in module, 已经import, 使用importlib.import_module 加载
    module = sys.modules.get(module_name, None)

    # # 尝试从程序文件所在目录加载指定包
    if module is None:
        try:
            yxcore_program_path=os.environ.get(SETTING_KEY.PROGRAM_FILE_PATH)
            if yxcore_program_path is not None and yxcore_program_path != '':
                yxcore_program_base_path = os.path.dirname(yxcore_program_path)
                module = load(os.path.join(yxcore_program_base_path, module_name))
        except ImportError as msg:
            # only ignore ImportError
            pass

    # 尝试从当前 YXCORE 路径加载指定包
    # 仅对 build-in module 有效
    if module is None:
        try:
            yxcore_lib_path=os.environ.get(SETTING_KEY.YXCORE_PATH)
            # yxcore_lib_path=os.environ.get('YXCORE_PATH')
            if yxcore_lib_path is not None and yxcore_lib_path != '':
                yxcore_lib_base_path = os.path.dirname(yxcore_lib_path)
                module = load(os.path.join(yxcore_lib_base_path, module_name))
        except ImportError as msg:
            # only ignore ImportError
            pass

    
    # 尝试从 PYTHONPATH 加载指定包
    if module is None:
        try:
            python_path_str=os.environ.get('PYTHONPATH')

            if python_path_str is not None and python_path_str != '':
                python_path_list=python_path_str.split(':')
                for python_path in python_path_list:

                    if python_path == '':
                        continue

                    module = load(os.path.join(python_path, module_name))
                    if module is not None:
                        break

        except ImportError as msg:
            # only ignore ImportError
            pass
                
        

    if module is None:
        raise ImportError('没有找到module:%s' % (module_name,))
    
    item = getattr(module, class_name, None)
    if item is None:
        raise ImportError('没有找到item:%s in module:%s' % (class_name, module_name))

    return item


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
