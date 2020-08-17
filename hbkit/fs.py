# -*- coding: utf-8 -*-
import click
import logging
from .libs.fs import Watcher, DummyScheme, GitScheme


@click.group('fs')
@click.pass_obj
def cli(g):
    """FileSystem management tools."""
    level = 'DEBUG' if g.verbose else 'INFO'
    logging.basicConfig(format='%(asctime)s >> %(message)s', level=level)


@cli.command('sync')
@click.argument('path', type=click.Path(exists=True, file_okay=False,
                                        dir_okay=True, resolve_path=True))
@click.option('--dummy', is_flag=True, help='Run dummy sync scheme.')
@click.option('--watch', is_flag=True,
              help='Run sync automatically when directory changes.')
@click.option('--timeout', default=300,
              help='Timeout seconds after watching with no changes.')
@click.option('--delay', default=3,
              help='Delay seconds when file changes detected.')
@click.option('--git-commit-message', default='Update on {hostname}',
              help='Git commit message template')
@click.option('--notify', is_flag=True,
              help='Show notification in notification center.')
def cli_sync(path, dummy, watch, timeout, delay, git_commit_message, notify):
    """Sync files in specified directory."""
    if dummy:
        scheme = DummyScheme(path, notify)
    else:
        scheme = decide_scheme(path, notify,
                               git_commit_message=git_commit_message)

    # First run
    scheme.process()
    if watch:
        watcher = Watcher(timeout, delay)
        while True:
            watcher.watch(path)
            scheme.process()
    click.echo('Done.')


def decide_scheme(path, notify, **kwargs):
    # TODO: Auto detect scheme
    return GitScheme(path, notify, commit_message=kwargs['git_commit_message'])
