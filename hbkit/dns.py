# -*- coding: utf-8 -*-
from __future__ import absolute_import
from builtins import *      # noqa
import click
import dns.resolver
from .lib import DNSPodClient


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
@click.option('--domain')
@click.pass_context
def cli(ctx, domain):
    """DNS Management Commands."""
    ns = dns.resolver.query(domain, 'NS')[0].to_text()
    if 'dnspod.net' in ns.lower():
        token = ctx.obj.config.get('dnspod.token')
        if not token:
            raise click.ClickException(
                'You need to setup {} in configuration'.format('dnspod')
            )
        ctx.obj = DNSPodClient(domain, token)
    else:
        raise click.ClickException(
            'DNS {} is not supported.'.format(ns)
        )


@cli.command('list')
@click.pass_obj
def cli_list(client, domain):
    """List all the dns records for domain."""
    for r in client.list():
        click.echo('* {0.name: <12} {0.type: <8} {0.value}'.format(r))


@cli.command('add')
@click.argument('name')
@click.argument('type', type=click.Choice(['A', 'CNAME']))
@click.argument('value')
@click.pass_obj
def cli_add(client, name, type, value):
    pass


@cli.command('set')
@click.argument('name')
@click.argument('type', type=click.Choice(['A', 'CNAME']))
@click.argument('value')
@click.pass_obj
def cli_set(client, name, type, value):
    pass


@cli.command('delete')
@click.argument('subdomain')
@click.pass_obj
def cli_delete(services, subdomain):
    pass
