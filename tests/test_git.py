# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from builtins import *      # noqa
import pytest
from hbkit import libs


@pytest.fixture
def git_config():
    content = \
"""
[core]
	repositoryformatversion = 0
	filemode = true
	bare = false
	logallrefupdates = true
	ignorecase = true
	precomposeunicode = true
[remote "origin"]
	url = https://github.com/graycarl/hbkit.git
	fetch = +refs/heads/*:refs/remotes/origin/*
[remote "other"]
	url = https://gitlab.com/graycarl/hbkit.git
	fetch = +refs/heads/*:refs/remotes/origin/*
[branch "master"]
	remote = origin
	merge = refs/heads/master
[branch "Github-Check-CI"]
	remote = origin
	merge = refs/heads/Github-Check-CI
"""
    return content


def test_iter_remote_from_git_config(git_config):
    remotes = list(libs.git.iter_remotes_from_git_config(git_config))
    expect = [
        'https://github.com/graycarl/hbkit.git',
        'https://gitlab.com/graycarl/hbkit.git'
    ]
    assert remotes == expect
