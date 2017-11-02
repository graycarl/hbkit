# -*- coding: utf-8 -*-
from __future__ import absolute_import
import click
from . import core, random, short, watch, git, backup

__version__ = '0.5'


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Current version is: ' + __version__)
    ctx.exit()


@click.group(context_settings=dict(obj={}))
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True,
              help='Print out current version.')
def cli():
    core.setup()


cli.add_command(random.cli, 'random')
cli.add_command(short.cli, 'short')
cli.add_command(watch.cli, 'watch-urls')
cli.add_command(git.cli, 'git')
cli.add_command(backup.cli, 'backup')
