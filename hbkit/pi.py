# -*- coding: utf-8 -*-
import click
import requests


@click.group('pi')
def cli():
    """Tools for Raspberry PI"""


@cli.command('publish-ip')
@click.option('--token')
def cli_publish_ip(token):
    """Sync IP to DNS"""
    # TODO: Argument token
    # TODO: Argument domain
    domain = 'home.graycarl.me'
    resp = requests.get('https://api.ipify.org', params=dict(format='json'))
    ip = resp.json()['ip']
    click.echo('Public IP: ' + ip)
    click.echo('Write to dns ({})'.format(domain))
    args = {'login_token': token, 'format': 'json'}
    resp = requests.post(
        'https://dnsapi.cn/Record.List',
        data=dict(domain='graycarl.me', **args)
    )
    for d in resp.json()['records']:
        if d['name'] == 'home':
            record = d
            break
    else:
        click.echo('Record is not found.')
        return
    if record['value'] == ip:
        click.echo('Domain IP Not Changed.')
        return
    click.echo('Update Domain IP: {} -> {}'.format(record['value'], ip))
    resp = requests.post(
        'https://dnsapi.cn/Record.Modify',
        data=dict(domain='graycarl.me', record_id=record['id'],
                  sub_domain='home', record_type='A', record_line=u'默认',
                  value=ip, **args))
    if resp.json()['status']['code'] == '1':
        click.echo('Done')
    else:
        click.echo('Update IP Failed: \n' + resp.json()['status']['message'])


