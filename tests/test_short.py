# -*- coding: utf-8 -*-
import mock
from click.testing import CliRunner
from hbkit import short


def test_short():
    runner = CliRunner()
    result = runner.invoke(short.cli, ['http://baidu.com'])


