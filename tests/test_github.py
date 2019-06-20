# -*- coding: utf-8 -*-
from __future__ import absolute_import
from builtins import *      # noqa
import mock
import copy
import arrow
import urllib.request
from hbkit import github, libs

travis_responses = {
    'branch': {
        "@href": u"/repo/13873553/branch/master",
        "@representation": u"standard",
        "@type": u"branch",
        "default_branch": True,
        "exists_on_github": True,
        "last_build": {
            "@href": u"/build/518788878",
            "@representation": u"minimal",
            "@type": u"build",
            "duration": 61,
            "event_type": u"push",
            "finished_at": u"2019-04-11T14:05:40Z",
            "id": 518788878,
            "number": u"86",
            "previous_state": u"passed",
            "private": False,
            "pull_request_number": None,
            "pull_request_title": None,
            "started_at": u"2019-04-11T14:05:02Z",
            "state": u"passed"
        },
        "name": u"master",
        "repository": {
            "@href": u"/repo/13873553",
            "@representation": u"minimal",
            "@type": u"repository",
            "id": 13873553,
            "name": u"hbkit",
            "slug": u"graycarl/hbkit"
        }
    },
    'build': {
        "@href": u"/build/518788878",
        "@permissions": {
            "cancel": False,
            "read": True,
            "restart": False
        },
        "@representation": u"standard",
        "@type": u"build",
        "branch": {
            "@href": u"/repo/13873553/branch/master",
            "@representation": u"minimal",
            "@type": u"branch",
            "name": u"master"
        },
        "commit": {
            "@representation": u"minimal",
            "@type": u"commit",
            "committed_at": u"2019-04-11T14:04:29Z",
            "compare_url": u"https://github.com/graycarl/hbkit/compare/....",
            "id": 156484214,
            "message": u"Update README.md",
            "ref": u"refs/heads/master",
            "sha": u"3207b8e34903913c5b7d77a5ce310ea1176e641d"
        },
        "created_by": {
            "@href": u"/user/527960",
            "@representation": u"minimal",
            "@type": u"user",
            "id": 527960,
            "login": u"graycarl"
        },
        "duration": 61,
        "event_type": u"push",
        "finished_at": u"2019-04-11T14:05:40Z",
        "id": 518788878,
        "jobs": [
            {
                "@href": u"/job/518788879",
                "@representation": u"minimal",
                "@type": u"job",
                "id": 518788879
            },
            {
                "@href": u"/job/518788880",
                "@representation": u"minimal",
                "@type": u"job",
                "id": 518788880
            }
        ],
        "number": u"86",
        "previous_state": u"passed",
        "private": False,
        "pull_request_number": None,
        "pull_request_title": None,
        "repository": {
            "@href": u"/repo/13873553",
            "@representation": u"minimal",
            "@type": u"repository",
            "id": 13873553,
            "name": u"hbkit",
            "slug": u"graycarl/hbkit"
        },
        "stages": [],
        "started_at": u"2019-04-11T14:05:02Z",
        "state": u"passed",
        "tag": None,
        "updated_at": u"2019-04-11T14:05:40.816Z"
    }
}


def mock_server(method, path):
    # Check for: https://github.com/graycarl/hbkit/issues/39
    urllib.request.urljoin(libs.GithubClient.travis_api, path)
    if method == 'get' and path.startswith('/repo'):
        data = copy.deepcopy(travis_responses['branch'])
    if method == 'get' and path.startswith('/build'):
        data = copy.deepcopy(travis_responses['build'])
    return data


def test_client_check_ci():
    c = libs.GithubClient()
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
    libs.GithubClient._request_travis = mock.Mock(side_effect=mock_server)
    g = mock.Mock(repo='name')
    result = runner.invoke(github.cli_check_ci, [], obj=g)
    assert 'Status: Passed' in result.output


def test_iter_github_repos_from_remotes():
    remotes = [
        'https://github.com/graycarl/aa.git',
        'http://github.com/graycarl/bb.git',
        'http://gitlab.com/graycarl/cc.git',
        'git@github.com:graycarl/dd.git',
        'git@other.com:graycarl/ee.git',
    ]
    expect = [
        'graycarl/aa',
        'graycarl/bb',
        'graycarl/dd'
    ]
    assert list(libs.github.iter_github_repos_from_remotes(remotes)) == expect
