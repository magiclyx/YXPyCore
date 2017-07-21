# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import sys
import traceback
import six

from yxcore import cmdline
from yxcore import logger
from yxcore import settings
from yxcore.utility import const
from yxcore.settings import SETTING_KEY
from yxcore.utility import loader
from yxcore.utility.exception import YXSettingErrorException, YXLauchErrorException


__author__ = 'yuxi'


APP_KEY = const.YXConstGenerator()
APP_KEY.CATEGORY_NAME = 'YXCOMMANDLINE'


class YXCoreApplication(object):
    """
    Application 的基类，继承的话要继承这个类
    """

    def __init__(self):
        self.name = None
        self.version = None
        self.cmdline = None
        self.entry = None

    def can_execute(self):
        return True if self.entry is not None else False

    def execute(self):
        if self.can_execute() is False:
            raise YXSettingErrorException('不是可自动运行的App')

        self.entry(self.cmdline)


_current_application = None


def initialize(argv=None):

    global _current_application

    if _current_application is not None:
        raise YXLauchErrorException('多次初始化')

    setting_path = os.environ.get(SETTING_KEY.ENVIRONMENT_SETTING_KEY)

    try:
        # 加载用户配置文件
        setting_module = loader.load(setting_path, SETTING_KEY.CUSTOM_SETTING_MODUE_NAME)

        # 显示的加载environment(此时可能已经加载过了)
        loader.load('yxcore.environment')

        # 显示的加载通知模块(此时可能已经加载过了)
        loader.load('yxcore.event')

        # 显示的加载日志模块(此时可能已经加载过了)
        loader.load('yxcore.logger')

        # 加载各个模块
        all_libs_name = getattr(setting_module, SETTING_KEY.INSTALLED_LIBS, [])
        for lib_name in all_libs_name:
            loader.load(lib_name)

        # 发送加载完毕消息
        settings.load_finished()

        # 解析命令行参数
        cmdline_value, prog_entry = cmdline.parse(argv)

        # 初始化一个YXCoreApplication 用于CurrentApplication
        app = YXCoreApplication()
        app.name = settings.setting_for_keypath(settings.path_join(APP_KEY.CATEGORY_NAME, 'name'))
        app.version = settings.setting_for_keypath(settings.path_join(APP_KEY.CATEGORY_NAME, 'version'))
        app.cmdline = cmdline_value
        app.entry = prog_entry

        _current_application = app

    except ImportError as msg:
        """注意，因为这里还没有初始化setting, 只能使用标准输出，输出错误"""
        logger.Std.error('can not load setting file(%s). \n%s\n%s' % (setting_path, msg, six.u(traceback.format_exc())))
        sys.exit(1)
    except Exception as msg:
        """注意，因为这里还没有初始化setting, 只能使用标准输出，输出错误"""
        six.print_(msg.message)
        logger.Std.error('unknown error on load:%s\n%s\n%s' % (setting_path, msg, six.u(traceback.format_exc())))
        sys.exit(1)

    return _current_application


def current_app():
    return _current_application


def execute_from_command_line(argv=None):

    """
    A simple method to run the app from settings
    """
    app = initialize(argv)
    app.execute()
