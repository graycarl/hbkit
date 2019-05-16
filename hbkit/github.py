# -*- coding: utf-8 -*-
from __future__ import absolute_import
from builtins import *      # noqa
import click
import arrow
import requests
import urllib.parse


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


class GithubClient(object):
    travis_api = 'https://api.travis-ci.org/'

    def __init__(self, token):
        self.token = token

    def _request_travis(self, method, path):
        headers = {
            'Travis-API-Version': '3',
            'User-Agent': 'hbkit',
        }
        url = urllib.request.urljoin(self.travis_api, path)
        resp = getattr(requests, method)(url, headers=headers)
        try:
            resp.raise_for_status()
        except requests.HTTPError:
            click.echo('Send request to travis api failed:\n' + resp.text)
            raise
        return resp.json()

    def check_ci(self, repo, branch='master'):
        path = 'repo/{}/branch/{}'.format(urllib.parse.quote_plus(repo), branch)
        resp = self._request_travis('get', path)
        resp = self._request_travis('get', resp['last_build']['@href'])
        lines = [
            'Status: {status}',
            'Built At: {time}',
            'Commit: [{commit_id}] {commit_msg}',
        ]
        data = dict(status=resp['state'].capitalize(),
                    time=arrow.get(resp['started_at']).to('local').isoformat(),
                    commit_id=resp['commit']['sha'][:10],
                    commit_msg=resp['commit']['message'])
        for line in lines:
            yield line.format(**data)

