# -*- coding: utf-8 -*-
from __future__ import absolute_import
from builtins import *      # noqa
import click


@click.group('mac')
def cli():
    """Tools for living in macOS."""


@cli.command('sync-spell')
def cli_sync_spell():
    """Sync LocalDictionary for current macOS user."""
