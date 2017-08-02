# -*- coding: utf-8 -*-
"""
hbkit watch-urls 'http://sample.com' --on timeout --timeout 10
hbkit watch-urls --on timeout,status --timeout 10 --status 404,502 < urls.txt
"""
import os
import sys
import click
import time
import requests
import datetime


def output(message):
    now = datetime.datetime.now()
    click.echo(u'[{}] {}'.format(now.strftime('%H:%M:%S'), message))


@click.command('watch-urls')
# @click.option('--on', required=True,
#               type=click.Choice(['timeout', 'status']),
#               multiple=True)
@click.option('--timeout', type=float, required=False, default=20.0)
@click.option('--interval', type=float, default=1.0)
@click.argument('urls', required=False, default=lambda: sys.stdin.read())
def cli(urls, timeout, interval):
    """Watch urls status."""
    urls = urls.strip().split(os.linesep)
    for i in range(len(urls)):
        if not urls[i].startswith('http'):
            urls[i] = 'http://' + urls[i]
        click.echo('Start to watch: {}'.format(urls[i]))

    try:
        while True:
            for url in urls:
                try:
                    rv = requests.get(url, timeout=timeout)
                    rv.raise_for_status()
                except requests.Timeout:
                    output('Timeout: {}'.format(url))
                except requests.HTTPError:
                    output('Status {}: {}'.format(rv.status_code, url))
                else:
                    click.echo('.', nl=False)
            time.sleep(interval)
    except KeyboardInterrupt:
        click.echo('Exit')
