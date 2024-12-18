from collections.abc import Iterator
import os
import collections
import configparser


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
    Item = collections.namedtuple('Item', ('key', 'value', 'default'))
    _bool_true_values = {'yes', 'on', 'true', '1'}
    _bool_false_values = {'no', 'off', 'false', '0'}

    class OptionNotFound(Exception):
        def __init__(self, key: str):
            self.key = key

    def __init__(self, path: str, defaults: dict):
        self.path = path
        self.defaults = defaults
        self.local = configparser.ConfigParser()
        self.local.read([path])

    def _parse_key(self, key: str) -> tuple[str, str]:
        try:
            section, option = key.split('.', 1)
        except ValueError:
            raise self.OptionNotFound(key)
        if not (section in self.defaults and option in self.defaults[section]):
            raise self.OptionNotFound(key)
        return section, option

    def list(self) -> Iterator[Item]:
        for section in self.defaults:
            for option in self.defaults[section]:
                try:
                    local = self.local[section][option]
                except KeyError:
                    local = None
                default = self.defaults[section][option]
                yield self.Item(section + '.' + option, local, default)

    def set(self, key: str, value: str) -> None:
        """Set local Value. None means delete the local key, using defaults."""
        section, option = self._parse_key(key)
        if value is None:
            self.local[section].pop(option, None)
            return
        if not isinstance(value, str):
            raise RuntimeError('Only string value is supportted.')
        if section not in self.local:
            self.local[section] = {}
        self.local[section][option] = value

    def get(self, key: str, type: type=str):
        if type not in (str, bool, int, float):
            raise RuntimeError('Unsupported type')
        section, option = self._parse_key(key)
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

    def save_to_file(self) -> None:
        try:
            configfile = open(self.path, 'w')
        # 暂时没法使用 Python3 的 FileNotFoundError，因为 Python2 没有这个定义
        # 且 Python-Future 暂时没有对它进行兼容。
        except IOError:
            os.makedirs(os.path.dirname(self.path))
            configfile = open(self.path, 'w')
        with configfile:
            self.local.write(configfile)
