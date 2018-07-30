# -*- coding: utf-8 -*-
from __future__ import absolute_import
from builtins import *      # noqa
import click
import arrow
import datetime

HUMAN_FORMAT = 'YYYY-MM-DD ddd HH:mm:ss ZZ'


@click.group('time')
def cli():
    """Tools about date & time."""


@cli.command('parse')
@click.argument('time_string')
def cli_parse(time_string):
    """Parse time string.
    The input time_string can be in any format, like iso6801 or timestamp etc.
    """
    naive_formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M:%S.%f',
        '%Y-%m-%d %H:%M',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M:%S.%f',
        '%Y-%m-%dT%H:%M',
    ]
    for f in naive_formats:
        try:
            naive_dt = datetime.datetime.strptime(time_string, f)
            time = arrow.get(naive_dt, 'local')
            break
        except ValueError:
            continue
    else:
        time = arrow.get(time_string)
    output(time)


def output(time):
    timestamp = u'TIMESTAMP: ' + str(time.timestamp)
    utc = u'ISO UTC: ' + time.to('utc').isoformat().replace('+00:00', 'Z')
    local = u'ISO LOCAL: ' + time.to('local').isoformat()
    human = u'HUMAN: ' + time.to('local').format(HUMAN_FORMAT)
    click.echo()
    click.echo(timestamp)
    click.echo(utc)
    click.echo(local)
    click.echo(human)
