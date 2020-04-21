# -*- coding: utf-8 -*-
import os
import click
from hbkit.libs import git


def parent_branch(repo, branch):
    return 'Parent'


@click.group('git')
@click.option('--path',
              type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.pass_context
def cli(ctx, path):
    """Tools for git."""
    try:
        import pygit2   # noqa
    except ImportError:
        click.echo("You need to install pygit2 before run this command")
        ctx.exit(1)
    if not path:
        path = os.path.abspath('.')
    root = git.find_root(path)
    if not root:
        click.echo("You're not in a git repository.")
        ctx.exit(1)
    ctx.obj.repo = pygit2.Repository(root)


@cli.command('parent-branch')
@click.argument('branch', required=False)
@click.pass_context
def cli_parent_branch(ctx, branch):
    repo = ctx.obj.repo
    if branch is None:
        branch = repo.head
    else:
        branch = repo.branches[branch]
    parent = parent_branch(repo, branch)
    click.echo('Parent branch is: {}'.format(parent.branch_name))


@cli.command('list-branch')
@click.pass_context
def cli_list_branch(ctx):
    for branch in ctx.obj.repo.branches:
        click.echo('* ' + branch)
