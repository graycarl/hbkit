# -*- coding: utf-8 -*-
from __future__ import absolute_import
import click
from . import core, random, short, watch

__version__ = '0.4'


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Current version is: ' + __version__)
    ctx.exit()


@click.group()
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True,
              help='Print out current version.')
def cli():
    core.setup()


cli.add_command(random.cli, 'random')
cli.add_command(short.cli, 'short')
cli.add_command(watch.cli, 'watch-urls')
