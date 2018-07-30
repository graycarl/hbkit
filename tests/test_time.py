# -*- coding: utf-8 -*-
from __future__ import absolute_import
from builtins import *      # noqa
import arrow
from click.testing import CliRunner
from hbkit import time
from hbkit.lib import Namespace


def test_parse_time():
    now = arrow.now()
    data = Namespace(
        arrow=now,
        timestamp=str(now.timestamp),
        utc=now.to('utc').isoformat().replace('+00:00', 'Z'),
        local=now.isoformat(),
        naive=now.to('local').naive.isoformat(' '),
        human=now.format(time.HUMAN_FORMAT)
    )
    runner = CliRunner()
    for key in ('utc', 'local', 'naive'):
        result = runner.invoke(time.cli_parse, [data[key]])
        print(result.output)
        assert ('ISO UTC: ' + data.utc) in result.output
        assert ('ISO LOCAL: ' + data.local) in result.output
        assert ('HUMAN: ' + data.human) in result.output
        assert ('TIMESTAMP: ' + data.timestamp) in result.output
    # When use timestamp as input, microsecond is lost
    now = now.replace(microsecond=0)
    data = Namespace(
        arrow=now,
        timestamp=str(now.timestamp),
        utc=now.to('utc').isoformat().replace('+00:00', 'Z'),
        local=now.isoformat(),
        naive=now.to('local').naive.isoformat(' '),
        human=now.format(time.HUMAN_FORMAT)
    )
    result = runner.invoke(time.cli_parse, [data.timestamp])
    print(result.output)
    assert ('ISO UTC: ' + data.utc) in result.output
    assert ('ISO LOCAL: ' + data.local) in result.output
    assert ('HUMAN: ' + data.human) in result.output
    assert ('TIMESTAMP: ' + data.timestamp) in result.output
