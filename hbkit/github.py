# -*- coding: utf-8 -*-
from __future__ import absolute_import
from builtins import *      # noqa
import os
import click
from hbkit import libs


@click.group('github')
@click.option('--repo', help='Github repo name.')
@click.pass_obj
def cli(g, repo):
    """Tools about github."""
    if not repo:
        root = libs.git.find_root(os.getcwd())
        if root:
            with open(os.path.join(root, '.git', 'config')) as f:
                remotes = libs.git.iter_remotes_from_git_config(f.read())
                try:
                    repo = next(
                        libs.github.iter_github_repos_from_remotes(remotes))
                    click.echo('Using repo from current project: %s' % repo)
                except StopIteration:
                    pass
    if not repo:
        repo = click.prompt('Repo')
    g.repo = repo


@cli.command('check-ci')
@click.argument('branch', default='master')
@click.pass_obj
def cli_check_ci(g, branch):
    """Get build status of trvis-ci."""
    client = libs.github.GithubClient(None)
    click.echo('\n'.join(client.check_ci(g.repo, branch)))
