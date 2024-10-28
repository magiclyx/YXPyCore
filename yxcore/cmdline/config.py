# -*- coding: utf-8 -*-

"""

使用 argparse 来提供命令行解析

命令行解析时，相关的参数

commandline_define - 这个是框架添加的参数，用于指出commandline 定义文件的位置
commandline_entry - 这个框架的入口, 只有当层的配置命中时, 才会调用当层的入口，这个不会继承

prog - 程序的名字 (default: sys.argv[0])
usage - 描述程序使用的字符串（默认：从添加到解析器的参数生成）
description - 在参数help之前显示的文本（默认值：none）
epilog - 在参数帮助后显示的文本（默认值：无）
parents - 还应包括其参数的ArgumentParser对象的列表
formatter_class - 用于自定义帮助输出的类
prefix_chars - 前缀可选参数的字符集（默认值：' - '）
fromfile_prefix_chars - 应读取附加参数的文件前缀的字符集（默认值：None）
argument_default - 参数的全局默认值（默认值：None）
conflict_handler - 解决冲突可选项的策略（通常不必要）
add_help - 为解析器添加-h / -help选项（默认值：True）
allow_abbrev - 如果缩写是明确的，则允许缩短长选项。（默认值：True）


对于每一个命令行参数，可以提供一下设置

名称或标志 - 名称或选项字符串列表，例如。foo或-f， - foo。
action - 在命令行遇到此参数时要执行的操作的基本类型。
nargs - 应该使用的命令行参数数。
const - 某些动作和nargs选择所需的常量值。
default - 如果参数在命令行中不存在，则生成的值。
type - 应转换命令行参数的类型。
choices - 参数的允许值的容器。
required - 是否可以省略命令行选项（仅可选）。
help - 参数的简要说明。
metavar - 使用消息中参数的名称。
dest - 要添加到由parse_args()返回的对象的属性的名称。

参数的定义，支持两中格式

一， 简单的参数定义
 = [
arguments 1,
arguments 2,
arguments 3
]



"""

import argparse

__author__ = 'yuxi'



# help信息中程序的名字(默认值None,等同于sys.argv[0])
prog = None

# help信息中的使用方法(一般不需要定义，默认是自动生成)
usage = None

# help信息中的描述
description = None

# commandline 最后的文字
epilog = ''

# 帮助信息格式(使用默认的HelpFormatter)
formatter_class = argparse.HelpFormatter

# 前缀可选参数集合
prefix_chars = '-'

# 应读取附加参数的文件前缀的字符集， 例如，设置为'@'， 则参数中任何以'@'开头的内容会被视为文件。会从这个文件中读取参数与命令行参数合并
fromfile_prefix_chars = None

# 参数的全局默认值（默认值：None）
argument_default = None

# 解决冲突可选项的策略（通常不必要. error 会抛出异常， 如果是resolve, 则新的参数会覆盖旧的参数)
conflict_handler = 'error'

# 是否自动添加 -h/--help 选项
add_help = True

# 如果缩写是明确的，则允许缩短长选项。（默认值：True）
allow_abbrev = True



