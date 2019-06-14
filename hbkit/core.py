# -*- coding: utf-8 -*-
from __future__ import absolute_import
from builtins import *      # noqa
import os
import sys
import logging
import click
import requests
from .libs import ConfigManager


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


class Group(click.Group):

    def main(self, *args, **kwargs):
        try:
            super(Group, self).main(*args, **kwargs)
        except requests.exceptions.SSLError as e:
            if sys.version.startswith('3') and \
                    'SSLV3_ALERT_HANDSHAKE_FAILURE' in str(e):
                message = [
                    "SSL lib may broken in current Python version.",
                    "You should install some additional package to fix it:",
                    "\t sudo apt install -y python3-dev libffi-dev libssl-dev",
                    "\t pip install requests[security]",
                    "See: https://stackoverflow.com/a/42028935",
                ]
                click.echo('\n'.join(message), err=True)
            raise
