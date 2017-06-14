# -*- coding: utf-8 -*-
from __future__ import absolute_import
import uuid
import click
import string
import random
import subprocess


def output(str):
    click.secho('Random Output:', fg='green')
    click.echo(str)
    if pbcopy:
        pipe = subprocess.Popen('pbcopy', stdin=subprocess.PIPE).stdin
        pipe.write(str)
        pipe.close()


@click.group('random')
@click.option('--copy', is_flag=True, help='Copy output to clipboard.')
def cli(copy):
    """Generate random string."""
    global pbcopy
    pbcopy = copy


@cli.command('string')
@click.argument('length', type=int)
def cli_string(length):
    """Generate random string."""
    src = string.ascii_letters
    chars = [random.choice(src) for i in range(length)]
    output(''.join(chars))


@cli.command('number')
@click.argument('length', type=int)
def cli_number(length):
    """Generate random number."""
    floor = int('1' + '0' * (length - 1))
    ceil = int('9' * length)
    output(str(random.randint(floor, ceil)))


@cli.command('uuid')
@click.option('--split', is_flag=True)
def cli_uuid(split):
    """Generate uuid."""
    u = uuid.uuid4()
    output(str(u) if split else u.hex)
