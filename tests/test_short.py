# -*- coding: utf-8 -*-
from hbkit import short


def test_short(runner):
    result = runner.invoke(short.cli, ['http://baidu.com'])
    result.output.strip().startswith('http')
