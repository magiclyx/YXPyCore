#!/usr/bin/env python -00
# -*- coding: utf-8 -*-

import sys


__author__ = 'yuxi'


if __name__ == "__main__":
    # 未配置环境变量时, 使用
    #os.environ.setdefault("YXCORE_SETTING_MODULE", os.path.join(os.path.dirname(__file__), 'config.py')) 

    from yxcore.application import execute_from_command_line

    execute_from_command_line(sys.argv)


def entry(cmdline):

    from yxcore import logger

    print(cmdline.workspace)
    print(cmdline.scheme)

    logger.warning('finished')



