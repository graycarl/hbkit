# -*- coding: utf-8 -*-
from __future__ import absolute_import
from builtins import *      # noqa
import click
import os
import time
import subprocess


@click.group('mac')
def cli():
    """Tools for living in macOS."""


@cli.command('sync-spell')
@click.pass_obj
def cli_sync_spell(g):
    """Sync LocalDictionary for current macOS user."""
    local_path = os.path.expanduser('~/Library/Spelling/LocalDictionary')
    remote_path = g.config.get('mac.remote_spell')
    remote_path = remote_path.replace('${icloud_path}',
                                      g.config.get('hbkit.icloud_path'))
    remote_path = os.path.expanduser(remote_path)
    with open(local_path, 'r') as f:
        local_words = set(map(str.strip, f.read().split()))
    with open(remote_path, 'r') as f:
        remote_words = set(map(str.strip, f.read().split()))
    click.echo('New from remote:')
    for w in (remote_words - local_words):
        click.echo(click.style('+ ' + w, fg='blue'))
    click.echo('New from local:')
    for w in (local_words - remote_words):
        click.echo(click.style('+ ' + w, fg='green'))
    with open(remote_path, 'w') as f:
        click.echo('Write to remote file ... ', nl=False)
        f.write(u'\n'.join(sorted(local_words | remote_words)) + '\n')
        click.echo('Done.')
    with open(local_path, 'w') as f:
        click.echo('Write to local file ... ', nl=False)
        f.write(u'\n'.join(sorted(local_words | remote_words)) + '\n')
        click.echo('Done.')
    click.echo('Stoping AppelSpell Daemon ... ', nl=False)
    resp = subprocess.run(['pgrep', 'AppleSpell'], stdout=subprocess.PIPE)
    old_pid = int(resp.stdout.strip())
    subprocess.run(['launchctl', 'stop', 'com.apple.applespell'], check=True)
    for i in range(20):
        time.sleep(0.3)
        resp = subprocess.run(['pgrep', 'AppleSpell'], stdout=subprocess.PIPE)
        if not resp.stdout.strip():
            click.echo('[{}] Stopped.'.format(old_pid))
            break
    else:
        click.echo(click.style('Stopping AppleSpell failed.', fg='red'))
        raise click.Abort
    click.echo('Restarting AppelSpell Daemon ... ', nl=False)
    subprocess.run(['launchctl', 'start', 'com.apple.applespell'], check=True)
    for i in range(20):
        time.sleep(0.3)
        resp = subprocess.run(['pgrep', 'AppleSpell'], stdout=subprocess.PIPE)
        if not resp.stdout.strip():
            continue
        new_pid = int(resp.stdout.strip())
        if new_pid == old_pid:
            continue
        click.echo('[{}] Started.'.format(new_pid))
        break
    else:
        click.echo(click.style('Restarting AppleSpell failed.', fg='red'))
        raise click.Abort
