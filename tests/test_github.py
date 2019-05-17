# -*- coding: utf-8 -*-
from __future__ import absolute_import
from builtins import *      # noqa
import mock
import copy
import arrow
from hbkit import github, lib

travis_responses = {
    'branch': {
        "@href": "/repo/13873553/branch/master",
        "@representation": "standard",
        "@type": "branch",
        "default_branch": True,
        "exists_on_github": True,
        "last_build": {
            "@href": "/build/518788878",
            "@representation": "minimal",
            "@type": "build",
            "duration": 61,
            "event_type": "push",
            "finished_at": "2019-04-11T14:05:40Z",
            "id": 518788878,
            "number": "86",
            "previous_state": "passed",
            "private": False,
            "pull_request_number": None,
            "pull_request_title": None,
            "started_at": "2019-04-11T14:05:02Z",
            "state": "passed"
        },
        "name": "master",
        "repository": {
            "@href": "/repo/13873553",
            "@representation": "minimal",
            "@type": "repository",
            "id": 13873553,
            "name": "hbkit",
            "slug": "graycarl/hbkit"
        }
    },
    'build': {
        "@href": "/build/518788878",
        "@permissions": {
            "cancel": False,
            "read": True,
            "restart": False
        },
        "@representation": "standard",
        "@type": "build",
        "branch": {
            "@href": "/repo/13873553/branch/master",
            "@representation": "minimal",
            "@type": "branch",
            "name": "master"
        },
        "commit": {
            "@representation": "minimal",
            "@type": "commit",
            "committed_at": "2019-04-11T14:04:29Z",
            "compare_url": "https://github.com/graycarl/hbkit/compare/....",
            "id": 156484214,
            "message": "Update README.md",
            "ref": "refs/heads/master",
            "sha": "3207b8e34903913c5b7d77a5ce310ea1176e641d"
        },
        "created_by": {
            "@href": "/user/527960",
            "@representation": "minimal",
            "@type": "user",
            "id": 527960,
            "login": "graycarl"
        },
        "duration": 61,
        "event_type": "push",
        "finished_at": "2019-04-11T14:05:40Z",
        "id": 518788878,
        "jobs": [
            {
                "@href": "/job/518788879",
                "@representation": "minimal",
                "@type": "job",
                "id": 518788879
            },
            {
                "@href": "/job/518788880",
                "@representation": "minimal",
                "@type": "job",
                "id": 518788880
            }
        ],
        "number": "86",
        "previous_state": "passed",
        "private": False,
        "pull_request_number": None,
        "pull_request_title": None,
        "repository": {
            "@href": "/repo/13873553",
            "@representation": "minimal",
            "@type": "repository",
            "id": 13873553,
            "name": "hbkit",
            "slug": "graycarl/hbkit"
        },
        "stages": [],
        "started_at": "2019-04-11T14:05:02Z",
        "state": "passed",
        "tag": None,
        "updated_at": "2019-04-11T14:05:40.816Z"
    }
}


def mock_server(method, path):
    if method == 'get' and path.startswith('/repo'):
        data = copy.deepcopy(travis_responses['branch'])
    if method == 'get' and path.startswith('/build'):
        data = copy.deepcopy(travis_responses['build'])
    return data


def test_client_check_ci():
    c = lib.GithubClient()
    c._request_travis = mock.Mock(side_effect=mock_server)
    lines = '\n'.join(c.check_ci('repo_name'))
    assert 'Status: Passed' in lines
    assert (
        'Built At: ' +
        arrow.get(travis_responses['build']['started_at'])
        .to('local').isoformat()) in lines
    assert ('Commit: [' + travis_responses['build']['commit']['sha'][:6]) \
        in lines
    c._request_travis.assert_any_call('get', '/repo/repo_name/branch/master')
    c._request_travis.assert_any_call(
        'get', travis_responses['branch']['last_build']['@href'])


def test_check_ci(runner):
    lib.GithubClient._request_travis = mock.Mock(side_effect=mock_server)
    g = mock.Mock(repo='name')
    result = runner.invoke(github.cli_check_ci, [], obj=g)
    assert 'Status: Passed' in result.output
