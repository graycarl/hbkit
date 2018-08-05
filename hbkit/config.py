# -*- coding: utf-8 -*-
from __future__ import absolute_import
from builtins import *      # noqa
import click
from . import core


@click.group('config')
def cli():
    """Commands about configuration management."""


@cli.command('list')
@click.option('--local', is_flag=True, help='Only local configurations.')
@click.option('--default', is_flag=True, help='Show default values.')
def cli_list(local, default):
    """List current settings."""
    line_format = '- [{key}]: {value}'
    options = []
    if default:
        header_line = 'Default settings:'
        options = [(i.key, i.default) for i in core.config.list()]
    elif local:
        header_line = 'Local settings:'
        options = [(i.key, i.value) for i in core.config.list()
                   if i.value is not None]
    else:
        header_line = 'Current settings:'
        options = map(
            lambda i: (i.key, i.default if i.value is None else i.value),
            core.config.list()
        )
    click.echo(header_line)
    for key, value in options:
        click.echo(line_format.format(key=key, value=value))


@cli.command('set')
@click.argument('key')
@click.argument('value', required=False)
def cli_set(key, value):
    """Set an option and save to local config file."""
    try:
        current_value = str(core.config.get(key))
    except core.config.OptionNotFound:
        raise click.UsageError('Unknown key: ' + key)
    if value is None:
        value = click.prompt('Value for "{}"'.format(key))
    core.config.set(key, value)
    click.echo('Option [{}] changed'.format(key))
    click.echo(click.style('  From: ' + current_value, fg='red'))
    click.echo(click.style('  TO  : ' + value, fg='green'))
    core.config.save_to_file()


@cli.command('unset')
@click.argument('key')
def cli_unset(key):
    """Unset an local option."""
    try:
        core.config.set(key, None)
    except core.config.OptionNotFound:
        raise click.UsageError('Unknown key: ' + key)
    click.echo('Option [{}] unseted'.format(key))
    core.config.save_to_file()
