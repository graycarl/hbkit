# -*- coding: utf-8 -*-
from __future__ import absolute_import
from builtins import *      # noqa
import os.path
from .lib import ConfigManager


config_defaults = {
    'dnspod': {
        'token': None,
    },
    'backup': {
        'dir': '~/iCloud/Backups/Automatic'
    }
}


class Global(object):
    """The global object passed by context."""

    def __init__(self, confpath, verbose=False):
        self.config = ConfigManager(
            os.path.expanduser(confpath), config_defaults)
        self.verbose = verbose
