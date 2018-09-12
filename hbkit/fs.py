# -*- coding: utf-8 -*-
from __future__ import absolute_import
from builtins import *      # noqa
import os
import click
import logging
import time as libtime
import platform
try:
    import pygit2
except ImportError:
    pygit2 = None


@click.group('fs')
@click.option('--debug', is_flag=True)
def cli(debug):
    """FileSystem management tools."""
    level = 'DEBUG' if debug else 'INFO'
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
        logging.info('Start watching.')
        try:
            libtime.sleep(self.timeout)
            logging.info('Timeout exceeded.')
        except KeyboardInterrupt:
            raise click.Abort


class SyncScheme(object):
    class ConflictFound(Exception):
        pass
    
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
            raise
        self.post_sync()


class GitScheme(SyncScheme):

    class Timeout(Exception):
        pass

    def __init__(self, path, commit_message):
        self.path = path
        self.commit_message = commit_message
        self._init_scheme(path)

    def _init_scheme(self, path):
        if not pygit2:
            click.echo(
                'This command need pygit2 to be installed.\n'
                'If you are in MacOS, do this:\n'
                '\n'
                '   brew install libgit2\n'
                '   pip install pygit2'
            )
            raise RuntimeError
            raise click.Abort

        self.repo = pygit2.Repository(path)

        class Callbacks(pygit2.RemoteCallbacks):
            def credentials(self, url, username_from_url, allowed_types):
                if allowed_types & pygit2.credentials.GIT_CREDTYPE_USERNAME:
                    return pygit2.Username("git")
                elif allowed_types & pygit2.credentials.GIT_CREDTYPE_SSH_KEY:
                    return pygit2.Keypair(
                        "git", os.path.expanduser('~/.ssh/id_rsa.pub'),
                        os.path.expanduser('~/.ssh/id_rsa'), "")
                else:
                    return None
        self.callbacks = Callbacks()

    def _commit_message(self):
        hostname = platform.node()
        return self.commit_message.format(**locals())

    def pre_sync(self):
        # check status
        status = self.repo.status()
        if any(map(lambda v: v & pygit2.GIT_STATUS_CONFLICTED,
                   status.values())):
            logging.warning('The repo is in conflict status, ignore syncing.')
            raise self.ConflictFound

    def confirm_local(self):
        author = self.repo.default_signature
        index = self.repo.index
        diff = index.diff_to_workdir()
        if not diff:
            logging.info('No local changes need to be committed.')
        else:
            logging.debug('Show Changes:\n%s', diff.patch)
            logging.info('Commit local changes.')
            index.add_all()
            index.write()
            tree_id = index.write_tree()
            message = self._commit_message()
            self.repo.create_commit('HEAD', author, author,
                                    message, tree_id, [self.repo.head.target])

    def fetch_remote(self):
        logging.info('Start to fetch from remote.')
        origin = self.repo.remotes['origin']
        origin.fetch(callbacks=self.callbacks)
        logging.debug('Fetch remote done.')

    def merge_changes(self):
        author = self.repo.default_signature
        # see: https://github.com/MichaelBoselowitz/pygit2-examples
        remote = self.repo.lookup_reference('refs/remotes/origin/master')
        result, _ = self.repo.merge_analysis(remote.target)
        if result & pygit2.GIT_MERGE_ANALYSIS_UP_TO_DATE:
            logging.info('Local files is up to date.')
        elif result & pygit2.GIT_MERGE_ANALYSIS_FASTFORWARD:
            logging.info('Processing fast-forward.')
            self.repo.checkout_tree(self.repo.get(remote.target))
            master = self.repo.lookup_reference('refs/heads/master')
            master.set_target(remote.target)
            self.repo.head.set_target(remote.target)
        elif result & pygit2.GIT_MERGE_ANALYSIS_NORMAL:
            logging.info('Merge remote and local changes.')
            self.repo.merge(remote.target)
            if self.repo.index.conflicts is not None:
                for conflict in self.repo.index.conflicts:
                    logging.warning('Conflicts found in:', conflict[0].path)
                raise self.ConflictFound

            tree = self.repo.index.write_tree()
            self.repo.create_commit(
                'HEAD', author, author, 'Merge!', tree,
                [self.repo.head.target, remote.target])
            # We need to do this or git CLI will think we are still merging.
            self.repo.state_cleanup()
        else:
            raise RuntimeError('Unknown result: %s' % result)

    def update_remote(self):
        remote = self.repo.lookup_reference('refs/remotes/origin/master')
        if self.repo.head.target == remote.target:
            logging.info('Remote is up to date.')
        else:
            logging.info('Pushing changes to remote.')
            origin = self.repo.remotes['origin']
            origin.push(['refs/heads/master:refs/heads/master'],
                        callbacks=self.callbacks)

    def update_local(self):
        pass


class FileSystemScheme(SyncScheme):
    """Sync with local directory."""


class DummyScheme(SyncScheme):

    def pre_sync(self):
        logging.info('Pre sync')

    def confirm_local(self):
        logging.info('Confirming local changes.')

    def fetch_remote(self):
        logging.info('Fetching remote changes.')

    def merge_changes(self):
        logging.info('Merge changes.')

    def update_remote(self):
        logging.info('Updateing remote.')

    def update_local(self):
        logging.info('Update local.')

    def post_sync(self):
        logging.info('Post sync.')


def decide_scheme(path, **kwargs):
    # TODO: Auto detect scheme
    return GitScheme(path, commit_message=kwargs['git_commit_message'])
