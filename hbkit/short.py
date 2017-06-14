# -*- coding: utf-8 -*-
import click
import requests


# From alfred workflow
SERVICES = {
    'bit.ly': {
        'url': 'https://api-ssl.bitly.com/v3/shorten',
        'params': {
            'format': 'json',
            'login': 'hzlzh',
            'apiKey': 'R_e8bcc43adaa5f818cc5d8a544a17d27d',
        },
        'key': 'longUrl',
        'response': lambda data: data['data']['url']
    },
    't.cn': {
        'url': 'https://api.weibo.com/2/short_url/shorten.json',
        'params': {
            'access_token': '2.00WSLtpB0GRHJ9745670860ceNWWiC',
            'source': '5786724301',
        },
        'key': 'url_long',
        'response': lambda data: data['urls'][0]['url_short']
    }
}


@click.command('short')
@click.option('--service', type=click.Choice(SERVICES.keys()),
              help='The service to use.',
              default='bit.ly')
@click.argument('url')
def cli(service, url):
    """Shorten your url."""
    if not url.startswith('http'):
        url = 'http://' + url
    service = SERVICES[service]
    params = {service['key']: url}
    params.update(service['params'])
    response = requests.get(service['url'], params=params)
    response.raise_for_status()
    click.echo(service['response'](response.json()))
