# -*- coding: utf-8 -*-
import click
import dns.resolver
from .libs.dns import DNSPodClient, DNSClient


@click.group('dns')
@click.option('--domain', prompt='Domain')
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
def cli_list(client):
    """List all the dns records for domain."""
    for r in client.list():
        click.echo('* {0.name: <12} {0.type: <8} {0.value}'.format(r))


@cli.command('add')
@click.argument('name')
@click.argument('type', type=click.Choice(['A', 'CNAME']))
@click.argument('value')
@click.pass_obj
def cli_add(client, name, type, value):
    """Add new record for domain."""
    record = DNSClient.Record(name, type, value)
    client.add(record)
    click.echo('New DNS Record Created.')


@cli.command('set')
@click.argument('name')
@click.argument('type', type=click.Choice(['A', 'CNAME']))
@click.argument('value')
@click.pass_obj
def cli_set(client, name, type, value):
    """Update a record for domain."""
    record = DNSClient.Record(name, type, value)
    try:
        client.set(record)
    except DNSClient.RecordNotFound:
        raise click.ClickException('Record is not Found.')
    click.echo('DNS Record Updated.')


@cli.command('delete')
@click.argument('name')
@click.option('--types', default='A,CNAME')
@click.pass_obj
def cli_delete(client, name, types):
    """Delete a record for domain."""
    types = types.upper().split(',')
    try:
        client.delete(name, types)
    except DNSClient.RecordNotFound:
        raise click.ClickException('Record is not Found.')
    click.echo('DNS Record Deleted.')
