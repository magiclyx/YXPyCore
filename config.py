# -*- coding: utf-8 -*-

import os
import argparse
from yxcore.cmdline import argument

__author__ = 'yuxi'


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_DIR = os.path.dirname(__file__)


# debug 模式
DEBUG = True


YXAPPLICATION = {
    'app_name': None,
    'version': '0.0.1',
}


# 安装的库文件
YXINSTALLED_LIBS = [
]


YXCOMMANDLINE = {

    'description': '工程分析工具, 使用 %(prog)s command --help 获得指定子命令的信息',
    'formatter_class': argparse.RawDescriptionHelpFormatter,
    'commandline_entry': 'example.entry',
    'commandline_define': [
        argument('--workspace', help='指定workspace', type=str, required=True),
        argument('--scheme', help='指定scheme', type=str, required=True),
    ]

}

# TODO loger 中支持 DEBUG 和 非DEBUG 模式的配置
YXLOGGER = {

    # default setting name
    'default_log_identifier': 'default_logger',

    # logger
    'loggers': {
        'default_logger': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'DEBUG',
        },
    },

}


# LINKMAP_DUMP_FILE = '/Users/yuxi/python/YXProjectAnalysis/log/linkmap'

