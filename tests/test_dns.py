# -*- coding: utf-8 -*-
import uuid
import pytest
from hbkit.libs.dns import DNSClient


class DummyClient(DNSClient):

    def __init__(self, *args, **kwargs):
        super(DummyClient, self).__init__(*args, **kwargs)

    def setup(self, values):
        self.records = [
            (uuid.uuid4().hex, name, type, value)
            for name, type, value in values
        ]

    def _fetch_all(self):
        return self.records

    def _process_add(self, name, type, value):
        self.records.append(
            (uuid.uuid4().hex, name, type, value)
        )

    def _process_remove(self, id):
        for row in list(self.records):
            if row[0] == id:
                self.records.remove(row)


def test_client_base_get():
    client = DummyClient('sample.com')
    client.setup([
        ('@', 'A', '1.1.1.1'),
        ('a', 'A', '2.2.2.2'),
        ('b', 'CNAME', 'a.b.c'),
        ('@', 'MX', 'mail.xx.com'),
    ])
    assert len(list(client.list())) == 4
    with pytest.raises(DNSClient.RecordNotFound):
        client.get('x')
    record = client.get('b')
    assert record.type == 'CNAME'
    assert record.value == 'a.b.c'
    with pytest.raises(DNSClient.RecordNotFound):
        client.get('b', ['A'])
    record = client.get('@', types=['A', 'CNAME'])
    assert record.type == 'A'
    assert record.value == '1.1.1.1'
    client.setup([
        ('a', 'A', '2.2.2.2'),
        ('b', 'CNAME', 'a.b.c'),
        ('@', 'MX', 'mail.xx.com'),
    ])
    with pytest.raises(DNSClient.RecordNotFound):
        client.get('@', ['A', 'CNAME'])


def test_client_base_add():
    client = DummyClient('sample.com')
    client.setup([
        ('a', 'A', '2.2.2.2'),
        ('b', 'CNAME', 'a.b.c'),
    ])
    with pytest.raises(DNSClient.DuplicatedRecord):
        client.add(DNSClient.Record('a', 'CNAME', 'xx.xx'))
    client.add(DNSClient.Record('c', 'CNAME', 'xx.xx'))
    assert len(list(client.list())) == 3
    record = client.get('c')
    assert record.value == 'xx.xx'

    client.setup([
        ('a', 'A', '2.2.2.2'),
        ('@', 'MX', 'mail.xx.com'),
    ])
    with pytest.raises(DNSClient.DuplicatedRecord):
        client.add(DNSClient.Record('@', 'MX', 'xx.xx'))
    client.add(DNSClient.Record('@', 'CNAME', 'xx.xx'))
    record = client.get('@', types=['A', 'CNAME'])
    assert record.type == 'CNAME'
    assert record.value == 'xx.xx'

    client.setup([
        ('a', 'A', '2.2.2.2'),
        ('@', 'CNAME', 'mail.xx.com'),
    ])
    with pytest.raises(DNSClient.DuplicatedRecord):
        client.add(DNSClient.Record('@', 'A', '8.8.8.8'))
    client.add(DNSClient.Record('@', 'MX', 'xx.xx'))


def test_client_base_set():
    client = DummyClient('sample.com')
    client.setup([
        ('a', 'A', '2.2.2.2'),
        ('b', 'CNAME', 'a.b.c'),
    ])
    with pytest.raises(DNSClient.RecordNotFound):
        client.set(DNSClient.Record('x', 'CNAME', 'xx.xx'))
    client.set(DNSClient.Record('b', 'CNAME', 'xx.xx'))
    a = client.get('a')
    assert a.type == 'A'
    b = client.get('b')
    assert b.value == 'xx.xx'
    assert len(list(client.list())) == 2


def test_client_base_delete():
    client = DummyClient('sample.com')
    client.setup([
        ('a', 'A', '2.2.2.2'),
        ('b', 'CNAME', 'a.b.c'),
    ])
    with pytest.raises(DNSClient.RecordNotFound):
        client.delete('x')
    with pytest.raises(DNSClient.RecordNotFound):
        client.delete('b', 'A')
    client.delete('b')
    assert len(list(client.list())) == 1


def test_client_base_valid_check():
    client = DummyClient('sample.com')
    client.setup([])
    client.add(DNSClient.Record('x', 'CNAME', 'a.b.c'))
    client.set(DNSClient.Record('x', 'A', '1.2.34.123'))
    client.add(DNSClient.Record('@', 'MX', 'a.b.c'))
    client.add(DNSClient.Record('@', 'A', '2.3.4.532'))
    client.set(DNSClient.Record('@', 'CNAME', 'a.b.c'))
    with pytest.raises(RuntimeError):
        client.add(DNSClient.Record('x', 'MX', 'a.b.c'))
    with pytest.raises(RuntimeError):
        client.add(DNSClient.Record('x', 'A', 'a.b.c'))
    with pytest.raises(RuntimeError):
        client.add(DNSClient.Record('x', 'CNAME', '3.4.5.6'))
    with pytest.raises(RuntimeError):
        client.add(DNSClient.Record('x', 'CNAME', 'inva#$domain'))
    with pytest.raises(RuntimeError):
        client.set(DNSClient.Record('x', 'XX', 'a.b.c'))
    with pytest.raises(RuntimeError):
        client.set(DNSClient.Record('@', 'XX', 'a.b.c'))
    with pytest.raises(RuntimeError):
        client.set(DNSClient.Record('@', 'A', 'a.b.c'))
    with pytest.raises(RuntimeError):
        client.set(DNSClient.Record('@', 'CNAME', '9.9.99.9'))
    with pytest.raises(RuntimeError):
        client.set(DNSClient.Record('x', 'XX', 'a.b.c'))


def test_dnspod():
    pass
