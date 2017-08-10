# -*- coding: utf-8 -*-
import os
import click


def parent_branch(repo, branch):
    return 'Parent'


pygit2_install_help = """\
This command need pygit2 to be installed.
If you are in MacOS, do this:

    brew install libgit2
    pip install pygit2
"""


@click.group('git')
@click.option('--path',
              type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.pass_context
def cli(ctx, path):
    """Tools for git."""
    try:
        import pygit2   # noqa
    except ImportError:
        click.echo(pygit2_install_help)
        ctx.exit(1)
    if not path:
        path = os.path.abspath('.')
        for i in range(8):
            if os.path.exists(os.path.join(path, '.git')):
                break
            path = os.path.dirname(path)
        else:
            click.echo("You're not in a git repository.")
            ctx.exit(1)
    ctx.obj['repo'] = pygit2.Repository(path)


@cli.command('parent-branch')
@click.argument('branch', required=False)
@click.pass_context
def cli_parent_branch(ctx, branch):
    repo = ctx.obj['repo']
    if branch is None:
        branch = repo.head
    else:
        branch = repo.branches[branch]
    parent = parent_branch(repo, branch)
    click.echo('Parent branch is: {}'.format(parent.branch_name))


@cli.command('list-branch')
@click.pass_context
def cli_list_branch(ctx):
    for branch in ctx.obj['repo'].branches:
        click.echo('* ' + branch)
