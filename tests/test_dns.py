# -*- coding: utf-8 -*-
from __future__ import absolute_import
from builtins import *      # noqa
import pytest
from hbkit.lib import DNSPodClient, DNSClient


class FakeClient(DNSClient):

    records = [
        DNSClient.DNSRecord('@', 'A', '1.1.1.1'),
        DNSClient.DNSRecord('a', 'A', '1.1.1.1'),
        DNSClient.DNSRecord('b', 'CNAME', 'a.b.c'),
        DNSClient.DNSRecord('@', 'MX', 'a.b.c'),
    ]

    def _find_same(self, record):
        if record.name == '@':
            if record.type == 'MX':
                def fn(r): return r.type == 'MX' and r.name == '@'
            else:
                def fn(r): return r.type != 'MX' and r.name == '@'
        else:
            def fn(r): return r.name == record.name
        try:
            return next(filter(fn, self.records))
        except StopIteration:
            return None

    def list(self):
        return sorted(self.records)

    def get(self, name):
        for r in self.records:
            if r.name == name:
                return r
        else:
            raise self.RecordNotFound(name)

    def add(self, record):
        self._check_valid(record)
        if self._find_same(record):
            raise self.DuplicatedRecord(record.name)
        self.records.append(record)

    def set(self, record):
        self._check_valid(record)
        current = self._find_same(record)
        if not current:
            raise self.RecordNotFound(record.name)
        self.records.pop(current)
        self.records.append(record)

    def delete(self, record):
        current = self._find_same(record)
        if not current:
            raise self.RecordNotFound(record.name)
        self.records.pop(current)


def test_client():
    pass


def test_dns():
    pass
