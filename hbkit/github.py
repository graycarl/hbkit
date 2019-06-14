# -*- coding: utf-8 -*-
from __future__ import absolute_import
from builtins import *      # noqa
import click
from hbkit.libs import GithubClient


@click.group('github')
@click.option('--repo', help='Github repo name.', prompt=True)
@click.pass_obj
def cli(g, repo):
    """Tools about github."""
    g.repo = repo


@cli.command('check-ci')
@click.argument('branch', default='master')
@click.pass_obj
def cli_check_ci(g, branch):
    """Get build status of trvis-ci."""
    client = GithubClient(None)
    click.echo('\n'.join(client.check_ci(g.repo, branch)))
