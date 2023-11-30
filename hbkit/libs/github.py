from collections.abc import Iterable
import re
import arrow
import logging
import urllib.parse
import requests


class GithubClient:

    travis_api = 'https://api.travis-ci.org/'
    logger = logging.getLogger('githubclient')

    def __init__(self, token: str | None = None):
        self.token = token

    def _request_travis(self, method: str, path: str) -> dict:
        headers = {
            'Travis-API-Version': '3',
            'User-Agent': 'hbkit',
        }
        url = urllib.parse.urljoin(self.travis_api, path)
        resp = getattr(requests, method)(url, headers=headers)
        try:
            resp.raise_for_status()
        except requests.HTTPError:
            self.logger.error('Call travis api failed: %s', resp.text)
            raise
        return resp.json()

    def check_ci(self, repo: str, branch: str = 'master') -> Iterable[str]:
        path = '/repo/{}/branch/{}'.format(
            urllib.parse.quote_plus(repo), branch
        )
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
                    commit_msg=resp['commit']['message'].split('\n')[0])
        for line in lines:
            yield line.format(**data)


def iter_github_repos_from_remotes(remotes: Iterable[str]) -> Iterable[str]:
    p = r'(https?://github.com/|git@github.com:)(\w+/\w+)\.git'
    for remote in remotes:
        match = re.match(p, remote)
        if match:
            yield match.group(2)
