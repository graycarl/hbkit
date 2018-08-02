# -*- coding: utf-8 -*-
from __future__ import absolute_import
from builtins import *      # noqa
import os.path
from .lib import ConfigManager


config = None


def setup(confpath):
    global config
    config = ConfigManager(os.path.expanduser(confpath), config_defaults)


config_defaults = {
    'domain': {
        'dnspod.token': None,
    },
    'backup': {
        'dir': '~/iCloud/Backups/Automatic'
    }
}
