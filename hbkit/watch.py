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


class Output(object):

    def __init__(self):
        self.ok_counter = 0

    def new_line(self):
        now = datetime.datetime.now()
        click.echo(u'\n[{}] '.format(now.strftime('%H:%M:%S')), nl=False)

    def ok(self):
        self.ok_counter += 1
        if self.ok_counter == 1:
            self.new_line()
        click.echo('.', nl=False)
        if self.ok_counter == 80:
            self.ok_counter = 0

    def boom(self, message):
        self.new_line()
        click.echo(message, nl=False)
        self.ok_counter = 0


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

    output = Output()
    try:
        while True:
            for url in urls:
                try:
                    rv = requests.get(url, timeout=timeout)
                    rv.raise_for_status()
                except requests.Timeout:
                    output.boom('Timeout: {}'.format(url))
                except requests.HTTPError:
                    output.boom('Status {}: {}'.format(rv.status_code, url))
                else:
                    output.ok()
            time.sleep(interval)
    except KeyboardInterrupt:
        click.echo('\nExit')
