# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import collections
from collections import deque
import six


__author__ = 'yuxi'


class BidirectionalIterator(object):
    """
    一个双向iterator
    普通的iterator 只提供了 next 方法
    """
    def __init__(self, collection):
        self.collection = collection
        self.index = 0

    def next(self):
        try:
            result = self.collection[self.index]
            self.index += 1
        except IndexError:
            raise StopIteration
        return result

    def prev(self):
        self.index -= 1
        if self.index < 0:
            raise StopIteration
        return self.collection[self.index]

    def preview_next(self):
        if self.has_next():
            return self.collection[self.index]
        else:
            raise StopIteration

    def preview_prev(self):
        if self.has_prev():
            return self.collection[self.index-1]
        else:
            raise StopIteration

    def has_next(self):
        return True if self.index+1 <= len(self.collection) else False

    def has_prev(self):
        return True if self.index > 0 else False

    def go_forward(self):

        if self.has_next():
            self.index += 1
        else:
            return False

    def go_back(self):

        if self.has_prev():
            return True
        else:
            return False

    def __iter__(self):
        return self


class RollbackIterator(object):

    def __init__(self, collection_or_iterator, max_rollback=1):
        """
        可以回滚的迭代器
        参数可以是容器或其他迭代器
        max_rollback 最大回滚次数。 如果为None则不限次数
        """

        self.buckup_queue = deque(maxlen=max_rollback)
        self.rollback_queue = deque()

        if isinstance(collection_or_iterator, collections.Iterator):
            self.it = collection_or_iterator
        elif isinstance(collection_or_iterator, collections.Iterable):
            self.it = iter(collection_or_iterator)
        else:
            raise TypeError('not a iterator or iterable obj')

    def __next__(self):
        if len(self.rollback_queue) is not 0:
            item = self.rollback_queue.popleft()
        else:
            item = six.next(self.it)  # #:~ python2 adaptation
        self.buckup_queue.append(item)
        return item

    def next(self):
        return self.__next__()

    def rollback(self, times=1):
        for time in range(0, times):
            item = self.buckup_queue.pop()
            self.rollback_queue.append(item)

    def __iter__(self):
        return self
