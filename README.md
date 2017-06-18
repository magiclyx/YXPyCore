# YXPyCore
一个 Python App 的框架


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

#### 安装的库
```python
YXINSTALLED_LIBS = [
'lib_A',
'lib_B'
'App_C'
]
```

#### 命令行解析
```python
YXCOMMANDLINE = []
```

#### 日志
```python
YXLOGGER = []
```