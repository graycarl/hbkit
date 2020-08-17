# -*- coding: utf-8 -*-
import re
import urllib
import logging
import collections
import requests


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
