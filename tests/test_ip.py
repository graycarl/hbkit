# -*- coding: utf-8 -*-
import requests
from hbkit import ip


class MockGet(object):

    class FakeResponse(object):
        def __init__(self, json):
            self._json = json

        def raise_for_status(self):
            pass

        def json(self):
            return self._json

    def __init__(self, responses):
        self.responses = responses

    def __call__(self, url, params, **kwargs):
        resp = self.responses[url]
        if isinstance(resp, Exception):
            raise resp
        return self.FakeResponse(resp)


def test_get_public(runner, monkeypatch):
    mock_get = MockGet({
        'https://httpbin.org/ip': {
            'origin': 'ip from httpbin',
        },
        'https://api.ipify.org': {
            'ip': 'ip from ipify',
        }
    })
    monkeypatch.setattr(requests, 'get', mock_get)
    # normal case
    result = runner.invoke(ip.cli_get_public).output.strip()
    assert result == 'ip from ipify'

    # ipify failed case
    mock_get.responses['https://api.ipify.org'] = requests.Timeout()
    result = runner.invoke(ip.cli_get_public).output.strip()
    assert result == 'ip from httpbin'

    # both failed case
    mock_get.responses['https://httpbin.org/ip'] = requests.Timeout()
    result = runner.invoke(ip.cli_get_public).output.strip()
    assert 'Can not get public IP' in result
