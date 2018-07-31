# -*- coding: utf-8 -*-
import requests
from hbkit import short


def _mock_get(url, params):

    class FakeResponse(object):
        def __init__(self, json):
            self._json = json

        def raise_for_status(self):
            pass

        def json(self):
            return self._json

    json = {
        'data': {
            'url': 'https://fake-short.com/123',
        }
    }
    return FakeResponse(json)


def test_short(runner, monkeypatch):
    monkeypatch.setattr(requests, 'get', _mock_get)
    result = runner.invoke(short.cli, ['http://baidu.com'])
    short_url = result.output.strip()
    assert 'https://fake-short.com' in short_url
