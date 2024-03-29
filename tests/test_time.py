# -*- coding: utf-8 -*-
from __future__ import absolute_import
from builtins import *      # noqa
import arrow
from hbkit import time
from hbkit.libs.datastructures import Namespace


def u(s):
    if not isinstance(s, str):
        return s.decode()
    return s


def test_parse_time(runner):
    now = arrow.now()
    data = Namespace(
        arrow=now,
        int_timestamp=str(now.int_timestamp),
        utc=u(now.to('utc').isoformat().replace('+00:00', 'Z')),
        local=u(now.isoformat()),
        naive=u(now.to('local').naive.isoformat(' ')),
        human=u(now.format(time.HUMAN_FORMAT))
    )
    for key in ('utc', 'local', 'naive'):
        result = runner.invoke(time.cli_parse, [data[key]])
        print(result.output)
        assert ('ISO UTC:   ' + data.utc) in result.output
        assert ('ISO LOCAL: ' + data.local) in result.output
        assert ('HUMAN:     ' + data.human) in result.output
        assert ('TIMESTAMP: ' + data.int_timestamp) in result.output
    # When use timestamp as input, microsecond is lost
    now = now.replace(microsecond=0)
    data = Namespace(
        arrow=now,
        int_timestamp=str(now.int_timestamp),
        utc=now.to('utc').isoformat().replace('+00:00', 'Z'),
        local=now.isoformat(),
        naive=now.to('local').naive.isoformat(' '),
        human=now.format(time.HUMAN_FORMAT)
    )
    result = runner.invoke(time.cli_parse, [data.int_timestamp])
    print(result.output)
    assert ('ISO UTC:   ' + data.utc) in result.output
    assert ('ISO LOCAL: ' + data.local) in result.output
    assert ('HUMAN:     ' + data.human) in result.output
    assert ('TIMESTAMP: ' + data.int_timestamp) in result.output


def test_parse_local_time_missing_second(runner):
    v = '2018-10-10 10:10'
    result = runner.invoke(time.cli_parse, [v])
    assert ('ISO LOCAL: ' + v.replace(' ', 'T')) in result.output
