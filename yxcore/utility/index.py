# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import itertools


__author__ = 'yuxi'


def generator(start=0, step=1):
    return lambda c=itertools.count(start, step): next(c)
