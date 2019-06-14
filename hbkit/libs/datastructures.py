# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from builtins import *      # noqa


class Namespace(dict):

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value
