import click
try:
    from pip import main as pipmain
except ImportError:
    from pip._internal import main as pipmain
    try:
        pipmain = pipmain.main
    except AttributeError:
        pass


@click.command('upgrade', help='Upgrade hbkit from github.')
@click.option('--source', default='https://github.com/graycarl/hbkit.git',
              help='Upgrade source')
def cli(source):
    source = 'git+' + source
    click.echo('Start upgrade from %s' % source)
    pipmain(['install', '--upgrade', source])
