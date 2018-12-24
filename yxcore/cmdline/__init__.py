# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import argparse
import sys
import os

from yxcore.utility import const, loader
from yxcore import settings
from yxcore.utility.exception import YXSettingErrorException

from yxcore.cmdline import config as default_config

__author__ = 'yuxi'

CMDLINE_KEY = const.YXConstGenerator()
CMDLINE_KEY.CATEGORY_NAME = 'YXCOMMANDLINE'


# 注册默认参数
settings.regist_default(CMDLINE_KEY.CATEGORY_NAME, 'prog', default_config.prog)
settings.regist_default(CMDLINE_KEY.CATEGORY_NAME, 'usage', default_config.usage)
settings.regist_default(CMDLINE_KEY.CATEGORY_NAME, 'description', default_config.description)
settings.regist_default(CMDLINE_KEY.CATEGORY_NAME, 'epilog', default_config.epilog)
settings.regist_default(CMDLINE_KEY.CATEGORY_NAME, 'formatter_class', default_config.formatter_class)
settings.regist_default(CMDLINE_KEY.CATEGORY_NAME, 'prefix_chars', default_config.prefix_chars)
settings.regist_default(CMDLINE_KEY.CATEGORY_NAME, 'fromfile_prefix_chars', default_config.fromfile_prefix_chars)
settings.regist_default(CMDLINE_KEY.CATEGORY_NAME, 'argument_default', default_config.argument_default)
settings.regist_default(CMDLINE_KEY.CATEGORY_NAME, 'conflict_handler', default_config.conflict_handler)
settings.regist_default(CMDLINE_KEY.CATEGORY_NAME, 'add_help', default_config.add_help)
settings.regist_default(CMDLINE_KEY.CATEGORY_NAME, 'allow_abbrev', default_config.allow_abbrev)


def argument(*argv, **kwargs):
    def _add2parser(parser):
        parser.add_argument(*argv, **kwargs)
    return _add2parser


def _walk_config(argv, config, parent=None):

    def _create_parser(*argv, **kwargs):
        """用于生成一个parser"""
        try:
            return argparse.ArgumentParser(*argv, **kwargs)
        except Exception as e:
            return argparse.ArgumentParser(*argv, **kwargs)

    def _add_cmdline(parser, cmdline_list):
        """用于将一个list中的param信息加入parser"""
        for cmdline in cmdline_list:
            cmdline(parser)

    # 拼装parent 列表
    parent = [parent] if parent is not None else []

    # 如果没有定义prog参数，则生成prog参数，因为子命令需要拼装 prog, 所以这里不使用默认的None。
    if 'prog' not in config or config['prog'] is None:
        config['prog'] = os.path.basename(sys.argv[0])

    # 删除config中的parent定义 (防止用户定义)
    config.pop('parents', None)  # 这要删掉配置中的parents

    # 取得程序入口，并从配置中删除 (这是我们自定义的属性，不能传入argparse)
    entry_point = config.pop('commandline_entry', None)

    # 获取all_command_line, 并从配置文件中删除 (这是我们自定义的属性，不能传入argparse)
    all_command_line = config.pop('commandline_define', None)
    if all_command_line is None:
        raise YXSettingErrorException('配置文件中，没有正确的配置commandline_define')

    # 如果是字符串配置的路径，这里要根据字符串加载(例如 'xx.xxx.setting.commandline')
    if isinstance(all_command_line, str):
        all_command_line = loader.item_by_path(all_command_line)

    # 开始解析命令行树
    if isinstance(all_command_line, list):

        config.pop('parents', None)  # 这要删掉配置中的parents
        cmdline_parser = _create_parser(parents=parent, **config)

        _add_cmdline(cmdline_parser, all_command_line)

        # 如果entry 是个字符串，尝试加载entry对应的函数
        if isinstance(entry_point, str):
            entry_point_string = entry_point
            entry_point = loader.item_by_path(entry_point_string)
            if entry_point is None:
                raise YXSettingErrorException('无法加载入口:%s' % (entry_point_string, ))

        return [cmdline_parser.parse_args(argv), entry_point]

    elif isinstance(all_command_line, dict):

        # 先生成root parser
        config.pop('add_help', None)  # 这里要删掉配置中的add_help
        root_parser = _create_parser(parents=parent, add_help=False, **config)

        # 配置root parser 的参数
        argument_list = [
            argument('command', nargs='?', choices=all_command_line.keys(), type=str, help='sub-command'),
        ]
        _add_cmdline(root_parser, argument_list)

        # 使用root, 解析命令行参数
        result = root_parser.parse_known_args(argv)

        # 获得子命令的配置(如果没有子命令或未找到对应的子命令，则打印错误信息并退出)
        sub_config = all_command_line.get(result[0].command, None)
        if sub_config is None:
            root_parser.print_help(file=sys.stderr)
            sys.exit(0)
            # raise YXSettingErrorException('配置文件中，没有正确的配置commandline_define')

        # 将自命令配置与当前命令配置合并, 使子命令的配置继承当前的配置 (使用 sub_config 中的信息，更新当前config的内容)
        merged_config = config.copy()
        merged_config.update(sub_config)

        # 替换prog 为 prog + command
        merged_config['prog'] = '%s %s' % (merged_config['prog'], result[0].command)

        # 递归调用，生成子parser
        return _walk_config(argv, merged_config, root_parser)


_cmdline_param = None
_program_entry = None


def parse(argv=None):

    global _cmdline_param
    global _program_entry

    if argv is None:
        argv = sys.argv[1:]
    else:
        argv = argv[1:]

    # 获取当前配置
    config = settings.setting_for_keypath(CMDLINE_KEY.CATEGORY_NAME)

    # 调用递归函数，解析配置
    _cmdline_param, _program_entry = _walk_config(argv, config)

    return [_cmdline_param, _program_entry]


def value():
    return _cmdline_param


def entry():
    return _program_entry
