# -*- coding: utf-8 -*-
from __future__ import absolute_import
from builtins import *      # noqa
import os
import re
import arrow
import urllib
import logging
import requests
import collections
import configparser


class Namespace(dict):

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value


class ConfigManager(object):
    """Configuration Manager.

    1. Read from ini file
    2. Write to ini file
    3. Support default values

    The ini file do not has a datatype concept, so ConfigManager also assume
    all key-value as string.

    :param path: the configuration file path to load.
    :param defaults: the default values for all configuration. like
                     `{'m1': {'key1': 'value1', 'key2': 'value2'}, 'm2': {}}`
    """
    Item = collections.namedtuple('ConfigItem', ('key', 'value', 'default'))
    _bool_true_values = {'yes', 'on', 'true', '1'}
    _bool_false_values = {'no', 'off', 'false', '0'}

    class OptionNotFound(Exception):
        def __init__(self, key):
            self.key = key

    def __init__(self, path, defaults):
        self.path = path
        self.defaults = defaults
        self.local = configparser.ConfigParser()
        self.local.read([path])

    def _parse_key(self, key):
        try:
            section, option = key.split('.', 1)
        except ValueError:
            raise self.OptionNotFound(key)
        if not (section in self.defaults and option in self.defaults[section]):
            raise self.OptionNotFound(key)
        return section, option

    def list(self):
        for section in self.defaults:
            for option in self.defaults[section]:
                try:
                    local = self.local[section][option]
                except KeyError:
                    local = None
                default = self.defaults[section][option]
                yield self.Item(section + '.' + option, local, default)

    def set(self, key, value):
        """Set local Value. None means delete the local key, using defaults."""
        section, option = self._parse_key(key)
        if value is None:
            self.local[section].pop(option, None)
            return
        if not isinstance(value, str):
            raise RuntimeError('Only string value is supportted.')
        if section not in self.local:
            self.local[section] = {}
        self.local[section][option] = value

    def get(self, key, type=str):
        if type not in (str, bool, int, float):
            raise RuntimeError('Unsupported type')
        section, option = self._parse_key(key)
        value = self.defaults[section][option]
        try:
            value = self.local[section][option]
        except KeyError:
            pass
        if type is str:
            return value
        elif type is bool:
            if value in self._bool_true_values:
                return True
            elif value in self._bool_false_values:
                return False
            else:
                raise ValueError('Wrong boolean string')
        else:
            return type(value)

    def save_to_file(self):
        try:
            configfile = open(self.path, 'w')
        # 暂时没法使用 Python3 的 FileNotFoundError，因为 Python2 没有这个定义
        # 且 Python-Future 暂时没有对它进行兼容。
        except IOError:
            os.makedirs(os.path.dirname(self.path))
            configfile = open(self.path, 'w')
        with configfile:
            self.local.write(configfile)


class DNSClient(object):

    logger = logging.getLogger('dnsclient')

    Record = collections.namedtuple(
        'DNSRecord', ('name', 'type', 'value'))
    _regex_ip = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    _regex_domain = re.compile(r'([-_\w]+\.)+[-_\w]+')

    class DuplicatedRecord(Exception):
        """Record already exists."""

    class RecordNotFound(Exception):
        """Record do not exists."""

    def __init__(self, domain):
        self.domain = domain

    def _check_valid(self, record):
        if record.name == '@' and record.type in ('A', 'CNAME', 'MX'):
            pass
        elif record.name != '@' and record.type in ('A', 'CNAME'):
            pass
        else:
            raise RuntimeError('Invalid DNS Type.')

        value_type = 'unknown'
        if self._regex_ip.match(record.value):
            value_type = 'ip'
        elif self._regex_domain.match(record.value):
            value_type = 'domain'

        if record.type == 'A' and value_type == 'ip':
            pass
        elif record.type in ('CNAME', 'MX') and value_type == 'domain':
            pass
        else:
            raise RuntimeError('Invalid DNS Value.')

    def _find_same(self, record, records):
        if record.name == '@':
            if record.type == 'MX':
                def fn(r): return r.type == 'MX' and r.name == '@'
            else:
                def fn(r): return r.type != 'MX' and r.name == '@'
        else:
            def fn(r): return r.name == record.name
        try:
            return next(filter(fn, records))
        except StopIteration:
            return None

    def _fetch_all(self):
        raise NotImplementedError

    def _process_add(self, name, type, value):
        raise NotImplementedError

    def _process_remove(self, id):
        raise NotImplementedError

    def list(self):
        for id, name, type, value in self._fetch_all():
            yield self.Record(name, type, value)

    def get(self, name, types=None, records=None):
        records = self.list() if records is None else records
        for r in records:
            if types is not None and r.type not in types:
                continue
            if r.name != name:
                continue
            return r
        else:
            raise self.RecordNotFound(name)

    def add(self, record):
        self._check_valid(record)
        if self._find_same(record, self.list()):
            raise self.DuplicatedRecord(record.name)
        self._process_add(record.name, record.type, record.value)

    def set(self, record):
        self._check_valid(record)
        records = {self.Record(name, type, value): id
                   for id, name, type, value in self._fetch_all()}
        current = self._find_same(record, records)
        if not current:
            raise self.RecordNotFound(record.name)
        self._process_remove(records[current])
        self._process_add(record.name, record.type, record.value)

    def delete(self, name, types=None):
        records = {self.Record(name, type, value): id
                   for id, name, type, value in self._fetch_all()}
        current = self.get(name, types)
        if not current:
            raise self.RecordNotFound(name)
        self._process_remove(records[current])


class DNSPodClient(DNSClient):

    urlbase = 'https://dnsapi.cn'

    def __init__(self, domain, token):
        self.argsbase = dict(login_token=token, format='json', domain=domain)

    def _request(self, path, data=None):
        url = urllib.parse.urljoin(self.urlbase, path)
        data = dict(self.argsbase, **data) if data else self.argsbase
        resp = requests.post(url, data=data)
        try:
            resp.raise_for_status()
        except requests.HTTPError:
            self.logger.error('Send request to dnspod failed:\n%s', resp.text)
            raise
        return resp.json()

    def _fetch_all(self):
        resp = self._request('Record.List')
        assert resp['status']['code'] == '1'
        for d in resp['records']:
            yield d['id'], d['name'], d['type'], d['value']

    def _process_add(self, name, type, value):
        data = dict(sub_domain=name, record_type=type, value=value,
                    record_line=u'默认')
        resp = self._request('Record.Create', data)
        assert resp['status']['code'] == '1'

    def _process_remove(self, id):
        resp = self._request('Record.Remove', dict(record_id=id))
        assert resp['status']['code'] == '1'


class GithubClient(object):

    travis_api = 'https://api.travis-ci.org/'
    logger = logging.getLogger('githubclient')

    def __init__(self, token=None):
        self.token = token

    def _request_travis(self, method, path):
        headers = {
            'Travis-API-Version': '3',
            'User-Agent': 'hbkit',
        }
        url = urllib.request.urljoin(self.travis_api, path)
        resp = getattr(requests, method)(url, headers=headers)
        try:
            resp.raise_for_status()
        except requests.HTTPError:
            self.logger.error('Call travis api failed: %s', resp.text)
            raise
        return resp.json()

    def check_ci(self, repo, branch='master'):
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
