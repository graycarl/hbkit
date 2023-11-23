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
        if time_string.lower() == 'now':
            time = arrow.now()
        elif time_string.isnumeric():
            time = arrow.get(float(time_string))
        else:
            time = arrow.get(time_string)
    output(time)


def output(time):
    lines = [
        ('TIMESTAMP: ' + str(time.int_timestamp)),
        ('ISO UTC:   ' + time.to('utc').isoformat().replace('+00:00', 'Z')),
        ('ISO LOCAL: ' + time.to('local').isoformat()),
        ('HUMAN:     ' + time.to('local').format(HUMAN_FORMAT))
    ]
    click.echo()
    for line in lines:
        name, content = line.split(':', 1)
        line = click.style(name + ':', fg='yellow') + content
        click.echo(line)
