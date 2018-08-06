# -*- coding: utf-8 -*-
from __future__ import absolute_import
from builtins import *      # noqa
import click
import dns.resolver
from .lib import Namespace, DNSPodClient


def _get_dns_client(services, domain):
    ns = dns.resolver.query(domain, 'NS')[0].to_text()
    if 'dnspod.net' in ns.lower():
        client_name = 'dnspod'
    else:
        raise click.ClickException(
            'DNS {} is not supported.'.format(ns)
        )
    if client_name not in services:
        raise click.ClickException(
            'You need to setup {} in configuration'.format(client_name)
        )
    return services[client_name]


@click.group('dns')
@click.pass_context
def cli(ctx):
    """DNS Management Commands."""
    services = Namespace()
    try:
        token = ctx.obj.config.get('dnspod.token')
        if token:
            services.dnspod = DNSPodClient(token)
    except ctx.obj.config.OptionNotFound:
        pass
    ctx.obj = services


@cli.command('list')
@click.argument('domain')
@click.pass_obj
def cli_list(services, domain):
    client = _get_dns_client(services, domain)
    click.echo('Use {}'.format(str(client)))
