# -*- coding: utf-8 -*-
from __future__ import absolute_import
from builtins import *      # noqa
import os
from .lib import ConfigManager


config_defaults = {
    'hbkit': {
        'icloud_path': os.environ.get(
            'ICLOUD_PATH', '~/Library/Mobile Documents/com~apple~CloudDocs/'
        ),
    },
    'dnspod': {
        'token': None,
    },
    'backup': {
        'dir': '${icloud_path}/Backups/Automatic'
    },
    'mac': {
        'remote_spell': '${icloud_path}/Settings/LocalDictionary'
    }
}


class Global(object):
    """The global object passed by context."""

    def __init__(self, confpath, verbose=False):
        self.config = ConfigManager(
            os.path.expanduser(confpath), config_defaults)
        self.verbose = verbose
