from __future__ import absolute_import, unicode_literals
from builtins import *      # noqa
import click
try:
    from pip import main as pipmain
except ImportError:
    from pip._internal import main as pipmain


@click.command('upgrade')
@click.option('--source', default='https://github.com/graycarl/hbkit.git',
              help='Upgrade source')
def cli(source):
    source = 'git+' + source
    click.echo('Start upgrade from %s' % source)
    pipmain(['install', '--upgrade', source])
