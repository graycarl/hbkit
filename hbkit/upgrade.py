import sys
import subprocess
import click


@click.command('upgrade', help='Upgrade hbkit from github.')
@click.option('--source', default='https://github.com/graycarl/hbkit.git',
              help='Upgrade source')
def cli(source):
    source = 'git+' + source
    click.echo('Start upgrade from %s' % source)
    subprocess.check_call(
        [sys.executable, '-m', 'pip', 'install', '--upgrade', source]
    )
