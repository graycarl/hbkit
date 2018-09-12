# -*- coding: utf-8 -*-
from __future__ import absolute_import
from builtins import *      # noqa
import click
import time as libtime


@click.group('fs')
def cli():
    """FileSystem management tools."""


@cli.command('sync')
@click.argument('path', type=click.Path(exists=True, file_okay=False,
                                        dir_okay=True))
@click.option('--dummy', is_flag=True, help='Run dummy sync scheme.')
@click.option('--watch', is_flag=True,
              help='Run sync automatically when directory changes.')
@click.option('--timeout', default=300,
              help='Timeout seconds after watching with no changes.')
@click.option('--delay', default=3,
              help='Delay seconds when file changes detected.')
@click.option('--git-commit-message', default='Update on {hostname}',
               help='Git commit message template')
def cli_sync(path, dummy, watch, timeout, delay, git_commit_message):
    """Sync files in specified directory."""
    if dummy:
        scheme = DummyScheme()
    else:
        scheme = decide_scheme(path, git_commit_message=git_commit_message)

    # First run
    scheme.process()
    if watch:
        watcher = Watcher(timeout, delay)
        while True:
            watcher.watch(path)
            scheme.process()
    click.echo('Done.')


class Watcher(object):

    def __init__(self, timeout, delay):
        self.timeout = timeout
        self.delay = delay

    def watch(self, path):
        try:
            libtime.sleep(self.timeout)
        except KeyboardInterrupt:
            raise click.Abort


class SyncScheme(object):

    def pre_sync(self):
        pass

    def confirm_local(self):
        raise NotImplementedError

    def fetch_remote(self):
        raise NotImplementedError

    def merge_changes(self):
        raise NotImplementedError

    def update_remote(self):
        raise NotImplementedError

    def update_local(self):
        raise NotImplementedError

    def post_sync(self):
        pass

    def process(self):
        self.pre_sync()
        try:
            self.confirm_local()
            self.fetch_remote()
            self.merge_changes()
            self.update_local()
            self.update_remote()
        except Exception:
            raise click.Abort
        self.post_sync()


class GitScheme(SyncScheme):

    def __init__(self, path, commit_message):
        self.path = path
        self.commit_message = commit_message
        self._check_dependency()

    def _check_dependency(self):
        try:
            import pygit2   # noqa
        except ImportError:
            click.echo(
                'This command need pygit2 to be installed.\n'
                'If you are in MacOS, do this:\n'
                '\n'
                '   brew install libgit2\n'
                '   pip install pygit2'
            )
            raise click.Abort


class DummyScheme(SyncScheme):

    def pre_sync(self):
        click.echo('Pre sync')

    def confirm_local(self):
        click.echo('Confirming local changes.')

    def fetch_remote(self):
        click.echo('Fetching remote changes.')

    def merge_changes(self):
        click.echo('Merge changes.')

    def update_remote(self):
        click.echo('Updateing remote.')

    def update_local(self):
        click.echo('Update local.')

    def post_sync(self):
        click.echo('Post sync.')


def decide_scheme(path, **kwargs):
    # TODO: Auto detect scheme
    return GitScheme(path, commit_message=kwargs['git_commit_message'])
