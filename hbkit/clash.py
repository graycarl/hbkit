# -*- coding: utf-8 -*-
import sys
import click
import pkg_resources
try:
    import yaml
except ImportError:
    yaml = None


@click.group('clash')
def cli():
    """Some tools about using clash"""
    if not yaml:
        raise click.ClickException(
            'You need to install pyyaml before run this command'
        )


@cli.command('build-config')
@click.option('--template', type=click.File('r', encoding='utf-8'),
              help='The template file.')
@click.option('--proxy-type',
              type=click.Choice([
                  'ss', 'vmess', 'http', 'snell', 'socks5', 'trojan']),
              help='Filter by proxy type')
@click.option('--reverse', is_flag=True,
              help='Reverse proxy order')
@click.argument('origin', type=click.File('r', encoding='utf-8'),
                default=sys.stdin)
def cli_build_config(template, origin, proxy_type, reverse):
    """Build new config from origin according to template"""
    if not template:
        template = pkg_resources \
            .resource_stream('hbkit', 'data/clash-template.yml') \
            .read() \
            .decode('utf-8')
    else:
        template = template.read()
    template = yaml.load(template)
    origin = yaml.load(origin.read())
    proxies = origin.get('proxies') or origin.get('Proxy')
    if proxy_type:
        proxies = list(filter(lambda p: p['type'] == proxy_type, proxies))
    if reverse:
        proxies = list(reversed(proxies))
    template['proxies'] = proxies
    for group in template['proxy-groups']:
        if group['name'] in ['FAST', 'FALLBACK', 'SPECIFY']:
            group['proxies'] = [p['name'] for p in proxies]
    click.echo(yaml.dump(template, allow_unicode=True))
