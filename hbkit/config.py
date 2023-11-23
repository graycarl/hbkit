import click


@click.group('config')
def cli():
    """Commands about configuration management."""


@cli.command('list')
@click.option('--local', is_flag=True, help='Only local configurations.')
@click.option('--default', is_flag=True, help='Show default values.')
@click.pass_obj
def cli_list(g, local, default):
    """List current settings."""
    line_format = '- [{key}]: {value}'
    options = []
    if default:
        header_line = 'Default settings:'
        options = [(i.key, i.default) for i in g.config.list()]
    elif local:
        header_line = 'Local settings:'
        options = [(i.key, i.value) for i in g.config.list()
                   if i.value is not None]
    else:
        header_line = 'Current settings:'
        options = map(
            lambda i: (i.key, i.default if i.value is None else i.value),
            g.config.list()
        )
    click.echo(header_line)
    for key, value in options:
        click.echo(line_format.format(key=key, value=value))


@cli.command('set')
@click.argument('key')
@click.argument('value', required=False)
@click.pass_obj
def cli_set(g, key, value):
    """Set an option and save to local config file."""
    try:
        current_value = str(g.config.get(key))
    except g.config.OptionNotFound:
        raise click.UsageError('Unknown key: ' + key)
    if value is None:
        value = click.prompt('Value for "{}"'.format(key))
    g.config.set(key, value)
    click.echo('Option [{}] changed'.format(key))
    click.echo(click.style('  From: ' + current_value, fg='red'))
    click.echo(click.style('  TO  : ' + value, fg='green'))
    g.config.save_to_file()


@cli.command('unset')
@click.argument('key')
@click.pass_obj
def cli_unset(g, key):
    """Unset an local option."""
    try:
        g.config.set(key, None)
    except g.config.OptionNotFound:
        raise click.UsageError('Unknown key: ' + key)
    click.echo('Option [{}] unseted'.format(key))
    g.config.save_to_file()
