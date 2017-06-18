# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from functools import partial
import six

__author__ = 'yuxi'


"""
同时适应python2 和 python3 的Singleton
"""


class _Singleton(type):
    """ A metaclass that creates a Singleton base class when called. """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# class Singleton(_Singleton('SingletonMeta', (object,), {})):
class Singleton(_Singleton(str('SingletonMeta'), (object,), {})):  # #:~ python2 adaptation
    pass


# 只支持 python2 的写法
# class Singleton(object):
#     __metaclass__ = _Singleton

# 只支持 python3 的写法
# class Singleton(metaclass=_Singleton):
#     pass


"""
一个装饰器，用于同时装饰类变量和实例变量
"""


class Automethod(object):
    """
    一个方法装饰器

    这个装饰器装饰的函数，既可以是类函数，也可以是成员函数。

    例如，定义下面这个类
    class Class2(object):
        @automethod
        def get_user(self, cls, msg):
            if self is None:
                print(('class method:%s-%s' % (cls, msg)))
            else:
                print(('instance method:%s-%s' % (self, msg)))

    我们以这种方法调用:
    Class2.get_user("###")
    Class2().get_user("###")

    会得到输出:
    class method:<class '__main__.Class2'>-###
    instance method:<__main__.Class2 object at 0x104db80f0>-###
    """

    # 旧的实现方式
    # def __get__(self, instance, owner=None):
    #     def wrapper(*args, **kwargs):
    #         return self.function(instance, owner, *args, **kwargs)
    #     return wrapper

    def __get__(self, instance, owner=None):
        return partial(self.function, instance, owner)

    def __init__(self, function):
        self.function = function


class switch(object):
    """
    实现的一个switch

    value: 要switch的值。 注意，如果这个值是可变的，必须要传一个可以调用的函数。使用lambda
    loop: 循环次数, 默认是1次。 和普通switch case 逻辑相同。 如果不是1次，则要在value 中传一个可以调用的函数。每次去取.


    v = 'ten'
    for case in switch(v):
        if case('one'):
            print 1
            break
        if case('two'):
            print 2
            break
        if case('ten'):
            print 10
            break
        if case('eleven'):
            print 11
            break
        if case(): # default, could also just omit condition or 'if True'
            print "something else!"
            # No need to break here, it'll stop anyway

    """

    def __init__(self, value, loop=1):

        if hasattr(value, '__call__'):
            self.value = None
            self.value_func = value
            self.loop = loop
        else:
            self.value_func = None
            self.value = value
            self.loop = 1  # always 1 in non func module

        self.fall = False

    def __iter__(self):

        if self.loop is not None:
            """Return the match method once, then stop"""
            for i in range(self.loop):
                self.fall = False  # reset context
                yield self.match
        else:
            while True:
                self.fall = False  # reset context
                yield self.match

        raise StopIteration

    def match(self, *args):

        if self.value_func is not None:
            value = self.value_func()
        else:
            value = self.value

        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif value in args:  # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False

def enumAuto(*sequential, **named):
    """
        TYPE = enumAuto('TYPE_A', 'TYPE_B', 'TYPE_C', )

        TYPE.TYPE_A
        ....
    """
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.iteritems())
    enums['reverse_mapping'] = reverse
    #return type('Enum'.encode(), (), enums)
    return type(str('Enum'), (), enums)


def enumDef(**enums):
    """
    _LMSectionType = enumDef(TYPE_A='A', TYPE_B='B', TYPE_C='C', )
    """
    reverse = dict((value, key) for key, value in enums.iteritems())
    enums['reverse_mapping'] = reverse
    return type(str('Enum'), (), enums)