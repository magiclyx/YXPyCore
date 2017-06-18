# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import weakref
import warnings
from functools import wraps
from yxcore import environment
from functools import partial
from yxcore.utility.exception import YXParameterErrorException
from yxcore.utility.warning import AsyncWarnging

# #:~ python2 adaptation
if environment.is_python3():
    from inspect import signature
else:
    from backports.inspect import signature


__author__ = 'yuxi'

__all__ = ['EventEngine', 'Event', 'regist', 'remove', 'send', 'post', 'event_handle']


class ObserverGroup(object):

    class Observer(object):
        def __init__(self, engine, receiver, sender, function, name):
            def recycle_fun(reference):
                self.engine.remove_observer(name, function)

            # 事件引擎
            self.engine = engine

            # 事件接收和发送方(接收方用于类方法，发送方用于约束只接收某实例发送的方法)
            self.receiver = weakref.proxy(receiver, recycle_fun) if receiver is not None else None
            self.sender = weakref.proxy(sender, recycle_fun) if sender is not None else None

            # 事件名称
            self.name = name

            # 响应事件的函数
            self.function = function

            # 响应函数是否是类中的方法(成员函数，类成员函数), 这里，静态函数是特里
            parameters = signature(function).parameters
            self.in_class = any(param_name in parameters for param_name in ['self', 'cls'])
            if self.in_class and sender is None:
                raise YXParameterErrorException("对于类中的函数, 如过不是静态函数，必须提供sender参数")

            # 响应函数是否忽略了event参数
            need_param = 1 if self.in_class else 0
            if len(parameters) == need_param:
                self.ignore_event_param = True
            elif len(parameters) == need_param + 1:
                self.ignore_event_param = False
            else:
                raise YXParameterErrorException("通知响应函数，最多只有一个参数")

        def allow(self, sender):
            if self.sender is not None:
                return self.sender == sender
            else:
                return True

        def trigger(self, sender, user_info):

            # 是否接受对应sender发送的消息
            if self.allow(sender) is False:
                return False

            # 引用返回用的function
            _function = self.function

            # 如果是类中的函数(类成员函数 或 类函数), 传入 self 或 cls 参数
            if self.in_class:
                if self.receiver is None:
                    return False  # 这里说明，类已经被释放了, 直接返回False, 不用发送通知了
                _function = partial(self.function, self.receiver)  # 注意，function 已经不是原来的function了

            # 如果函数没有忽略event参数，则传入event参数
            if self.ignore_event_param is False:
                _function = partial(_function, Event(self.name, sender, user_info))  # 注意，function 已经不是原来的function了

            # 调用function
            _function()

            return True

    def __init__(self, name):
        self.name = name
        self.group = dict()

    def add(self, engine, receiver, sender, function):
        observer = ObserverGroup.Observer(engine, receiver, sender, function, self.name)
        self.group[function] = observer

        return observer

    def remove(self, function):
        self.group.pop(function)

    def trigger(self, sender=None, **kwargs):

        # 用于map 遍历每个function
        def observer_walker(function):

            observer = self.group.get(function, None)
            if observer is None:
                return False

            return observer.trigger(sender, kwargs.get('userInfo', None))

        # 注意:python3 map 不会遍历列表，只是返回iterator。 要使用list强制遍历
        list(map(observer_walker, self.group))


class Event(object):
    """
    事件。 发送给事件回掉函数的参数
    """

    def __init__(self, name, sender, user_info):
        self.name = name
        self.sender = sender
        self.userInfo = user_info


class EventEngine(object):
    """
    分发事件的引擎
    """

    def __init__(self):
        self.event_dict = dict()

    # 支持参数 sender=xxx, 只接受xxx发送的事件
    def regist(self, name, function, receiver=None, **kwargs):
        # 第一层，使用事件名称索引 ObserverGroup
        observer_group = self.event_dict.setdefault(name, ObserverGroup(name))
        # 向 ObserverGroup 中添加一个观察者
        observer_group.add(self, receiver, kwargs.get('sender', None), function)

    def remove(self, name, function):
        observer_group = self.event_dict.get(name, None)
        if observer_group is not None:
            observer_group.remove(function)

    # 支持参数 userInfo=xxx, 额外传递参数
    def send(self, name, sender=None, **kwargs):

        group = self.event_dict.get(name, None)
        if group is None:
            return

        # 设置 remain 属性
        group.remain = kwargs.get('remain', False)

        # 触发s事件
        group.trigger(sender, **kwargs)

    # 支持参数 userInfo=xxx, 额外传递参数
    def post(self, name, sender=None, **kwargs):
        warnings.warn('通知不支持异步调用', AsyncWarnging)
        self.send(name, sender, **kwargs)


"""默认通知中心"""
default_engine = EventEngine()


# 支持参数 sender=xxx, 只接受xxx发送的事件
def regist(name, function, receiver=None, **kwargs):
    default_engine.regist(name, function, receiver, **kwargs)


def remove(name, function):
    default_engine.remove(name, function)


# 支持参数 userInfo=xxx, 额外传递参数
def send(name, sender=None, **kwargs):
    default_engine.send(name, sender, **kwargs)


# 支持参数 userInfo=xxx, 额外传递参数
def post(name, sender=None, **kwargs):
    default_engine.post(name, sender, **kwargs)


# 支持参数 sender=xxx, 只接受xxx发送的事件
# 支持参数 engine=xxx, 使用指定的时间引擎　
def event_handle(name, receiver=None, **kwargs):
    def _event_handle(func):

        engine = kwargs.get('engine', None)
        if engine is not None:
            engine.regist(name, func, receiver, **kwargs)
        else:
            default_engine.regist(name, func, receiver, **kwargs)

        @wraps(func)
        def ___event_handle():
            print('before')
            func()
            print('after')
        return ___event_handle

    return _event_handle
