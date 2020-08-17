# -*- coding: utf-8 -*-
import click
import os
import sys
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
    old_pid = int(subprocess.check_output(['pgrep', 'AppleSpell']))
    subprocess.check_call(['launchctl', 'stop', 'com.apple.applespell'])
    for i in range(20):
        time.sleep(0.3)
        try:
            subprocess.check_output(['pgrep', 'AppleSpell'])
        except subprocess.CalledProcessError:
            click.echo('[{}] Stopped.'.format(old_pid))
            break
    else:
        click.echo(click.style('Stopping AppleSpell failed.', fg='red'))
        raise click.Abort
    click.echo('Restarting AppelSpell Daemon ... ', nl=False)
    subprocess.check_call(['launchctl', 'start', 'com.apple.applespell'])
    for i in range(20):
        time.sleep(0.3)
        try:
            output = subprocess.check_output(['pgrep', 'AppleSpell'])
        except subprocess.CalledProcessError:
            continue
        new_pid = int(output.strip())
        if new_pid == old_pid:
            continue
        click.echo('[{}] Started.'.format(new_pid))
        break
    else:
        click.echo(click.style('Restarting AppleSpell failed.', fg='red'))
        raise click.Abort


@cli.command('notify')
@click.option('--title', default='New notification',
              help='Notification title.')
@click.argument('content', default=lambda: sys.stdin.read())
def cli_notify(title, content):
    """Show notification in Notification Center."""
    script = u'display notification "{content}" with title "{title}"'
    script = script.format(**locals())
    subprocess.call(['/usr/bin/osascript', '-e', script])
