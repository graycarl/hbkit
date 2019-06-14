# -*- coding: utf-8 -*-
from __future__ import absolute_import
import click
from future.standard_library import install_aliases
install_aliases()

from . import core, random, short, watch, git, backup, time, config, ip  # noqa
from . import dns, mac, fs, github   # noqa


__version__ = '0.9.2'


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Current version is: ' + __version__)
    ctx.exit()


@click.group(cls=core.Group)
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True,
              help='Print out current version.')
@click.option('--config', 'confpath',
              type=click.Path(dir_okay=False),
              help='The config file path.',
              default='~/.config/hbkit/hbkit.ini', show_default=True)
@click.option('--verbose', '-v', is_flag=True, help='Print execution details.')
@click.pass_context
def cli(context, confpath, verbose):
    context.obj = core.Global(confpath, verbose=verbose)


cli.add_command(random.cli, 'random')
cli.add_command(short.cli, 'short')
cli.add_command(watch.cli, 'watch-urls')
cli.add_command(git.cli, 'git')
cli.add_command(backup.cli, 'backup')
cli.add_command(time.cli, 'time')
cli.add_command(config.cli, 'config')
cli.add_command(ip.cli, 'ip')
cli.add_command(dns.cli, 'dns')
cli.add_command(mac.cli, 'mac')
cli.add_command(fs.cli, 'fs')
cli.add_command(github.cli, 'github')
