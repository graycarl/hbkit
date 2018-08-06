# -*- coding: utf-8 -*-
from __future__ import absolute_import
from builtins import *      # noqa
import click
import dns.resolver


def _get_domain_ns(domain):
    return dns.resolver.query(domain, 'NS')[0].target


@click.group('domain')
def cli():
    """Domain Management Commands."""
