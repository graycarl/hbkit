# -*- coding: utf-8 -*-
from __future__ import absolute_import
from builtins import *      # noqa
import collections
import configparser


class Namespace(dict):

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value


class ConfigManager(object):
    """Configuration Manager.

    1. Read from ini file
    2. Write to ini file
    3. Support default values

    The ini file do not has a datatype concept, so ConfigManager also assume
    all key-value as string.

    :param path: the configuration file path to load.
    :param defaults: the default values for all configuration. like
                     `{'m1': {'key1': 'value1', 'key2': 'value2'}, 'm2': {}}`
    """
    Item = collections.namedtuple('ConfigItem', ('key', 'value', 'default'))
    _bool_true_values = {'yes', 'on', 'true', '1'}
    _bool_false_values = {'no', 'off', 'false', '0'}

    def __init__(self, path, defaults):
        self.path = path
        self.defaults = defaults
        self.local = configparser.ConfigParser()
        self.local.read([path])

    def list(self):
        for section in self.defaults:
            for option in self.defaults[section]:
                try:
                    local = self.local[section][option]
                except KeyError:
                    local = None
                default = self.defaults[section][option]
                yield self.Item(section + '.' + option, local, default)

    def set(self, key, value):
        """Set local Value. None means delete the local key, using defaults."""
        section, option = key.split('.', 1)
        if value is None:
            self.local[section].pop(option, None)
            return
        if not isinstance(value, str):
            raise RuntimeError('Only string value is supportted.')
        if not (section in self.defaults and option in self.defaults[section]):
            raise KeyError(key)
        if section not in self.local:
            self.local[section] = {}
        self.local[section][option] = value

    def get(self, key, type=str):
        if type not in (str, bool, int, float):
            raise RuntimeError('Unsupported type')
        section, option = key.split('.', 1)
        value = self.defaults[section][option]
        try:
            value = self.local[section][option]
        except KeyError:
            pass
        if type is str:
            return value
        elif type is bool:
            if value in self._bool_true_values:
                return True
            elif value in self._bool_false_values:
                return False
            else:
                raise ValueError('Wrong boolean string')
        else:
            return type(value)

    def save_to_file(self):
        with open(self.path, 'w') as configfile:
            self.local.write(configfile)
