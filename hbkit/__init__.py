# -*- coding: utf-8 -*-
from __future__ import absolute_import
import click
from . import core, random, short, watch, git, backup, pi, time, config, ip

__version__ = '0.7.0'


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Current version is: ' + __version__)
    ctx.exit()


@click.group(context_settings=dict(obj={}))
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True,
              help='Print out current version.')
@click.option('--config', 'confpath',
              type=click.Path(dir_okay=False),
              help='The config file path.',
              default='~/.config/hbkit/hbkit.ini', show_default=True)
def cli(confpath):
    core.setup(confpath)


cli.add_command(random.cli, 'random')
cli.add_command(short.cli, 'short')
cli.add_command(watch.cli, 'watch-urls')
cli.add_command(git.cli, 'git')
cli.add_command(backup.cli, 'backup')
cli.add_command(pi.cli, 'pi')
cli.add_command(time.cli, 'time')
cli.add_command(config.cli, 'config')
cli.add_command(ip.cli, 'ip')
