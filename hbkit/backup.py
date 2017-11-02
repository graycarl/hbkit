# -*- coding: utf-8 -*-
import os
import click
import zipfile
import datetime


@click.command('backup')
@click.argument('path', type=click.Path(exists=True))
def cli(path):
    """Make a backup copy for file or directory."""
    now = datetime.datetime.now()
    date = now.strftime('%Y%m%d%H%M')
    files = []
    metadata = None
    if os.path.isfile(path):
        basename = os.path.basename(path)
        name, ext = os.path.splitext(basename)
        zipname = '{}-{}{}.zip'.format(name, date, ext)
        files.append(
            (path, basename)
        )
        metadata = 'origin-path: {}'.format(path)
    else:
        raise NotImplementedError

    # TODO: Configurable
    backup_dir = '~/iCloud/Backups/Automatic'
    zipname = os.path.join(os.path.expanduser(backup_dir), zipname)

    if os.path.exists(zipname):
        raise click.ClickException('Backup file already exists.')

    with zipfile.ZipFile(zipname, 'w') as zip:
        for path, name in files:
            zip.write(path, name)
        zip.writestr('backup-metadata.txt', metadata)

    click.echo('New backup created: [{}]'.format(zipname))
