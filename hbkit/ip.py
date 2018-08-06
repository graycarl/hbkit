# -*- coding: utf-8 -*-
from __future__ import absolute_import
from builtins import *      # noqa
import click
import requests


SERVICES = {
    'httpbin': {
        'url': 'https://httpbin.org/ip',
        'response': lambda data: data['origin']
    },
    'ipify': {
        'url': 'https://api.ipify.org',
        'params': {
            'format': 'json'
        },
        'response': lambda data: data['ip']
    }
}


@click.group('ip')
def cli():
    """Tools about ip address."""


@cli.command('get-public')
@click.option('--timeout', default=5.0, help='Timeout for network requests.')
def cli_get_public(timeout):
    """Get current public IP."""
    for name in ('ipify', 'httpbin'):
        service = SERVICES[name]
        response = requests.get(service['url'], params=service.get('params'),
                                timeout=timeout)
        response.raise_for_status()
        ip = service['response'](response.json())
        break
    else:
        raise click.ClickException('Can not get public IP')
    click.echo(ip)
