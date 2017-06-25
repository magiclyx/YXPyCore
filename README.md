# YXPyCore
一个 Python App 的框架

## Python
支持Python2 和 Python3

## 安装
`pip install -r requirements`

## 部署
添加 demo.py文件


```python
if __name__ == "__main__":
    from yxcore.application import execute_from_command_line
    execute_from_command_line(sys.argv)
```


程序会查找环境变量中YXCORE_SETTING_MODULE所指向的配置文件。如果同时部署了多个app，需要制定配置文件路径

```python
if __name__ == "__main__":
    os.environ.setdefault("YXCORE_SETTING_MODULE", "config")
    from yxcore.application import execute_from_command_line
    execute_from_command_line(sys.argv)
```

## 基本配置

#### App 信息
```python
YXAPPLICATION = {
    'app_name': None,
    'version': '0.0.1',
}
```

#### 调试模式
```python
DEBUG = True
```

#### 安装的程序包
```python
YXINSTALLED_LIBS = [
'lib_A',
'lib_B'
'App_C'
]
```

#### 命令行解析
```python
# 一个非常简单的命令行配置(非子命令)
YXCOMMANDLINE = {
    'description': '描述信息, 使用 %(prog)s command --help 获得指定子命令的信息',
    'formatter_class': argparse.RawDescriptionHelpFormatter,
    'commandline_define': [
        argument('--workspace', help='指定workspace', type=str, required=True),
        argument('--scheme', help='指定scheme', type=str, required=True),
    ],
}
```

#### 日志
```python
# 一个非常简单的指向标准输出的日志配置
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
```

#### 详细信息
[参看wiki](https://github.com/magiclyx/YXPyCore/wiki)
