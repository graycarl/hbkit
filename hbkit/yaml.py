import sys
import json
import click
try:
    import yaml
except ImportError:
    yaml = None


@click.group('yaml')
def cli():
    """Tools about parsing yaml files."""
    if not yaml:
        raise click.ClickException(
            'You need to install pyyaml before run this command'
        )


@cli.command('from-json')
@click.argument('input', type=click.File('r'), default=sys.stdin)
def cli_from_json(input):
    """Generate yaml string from json content."""
    data = json.loads(input.read())
    click.echo(yaml.safe_dump(data, allow_unicode=True))


@cli.command('to-json')
@click.argument('input', type=click.File('r'), default=sys.stdin)
def cli_to_json(input):
    data = yaml.safe_load(input.read())
    click.echo(json.dumps(data, indent=2, ensure_ascii=False))
