import sys
import click
from collections import OrderedDict
from importlib import resources
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
        template = resources.read_text('hbkit.data', 'clash-template.yml')
    else:
        template = template.read()
    template = ordered_load(template)
    origin = ordered_load(origin.read())
    proxies = origin.get('proxies') or origin.get('Proxy')
    if proxy_type:
        proxies = list(filter(lambda p: p['type'] == proxy_type, proxies))
    if reverse:
        proxies = list(reversed(proxies))
    template['proxies'].extend(proxies)
    for group in template['proxy-groups']:
        if group['name'] in ['FAST', 'FALLBACK', 'SPECIFY']:
            group['proxies'].extend([p['name'] for p in proxies])
    click.echo(ordered_dump(template, allow_unicode=True))


# Use OrderedDict to keep key-value order in yaml file.
# Got solution from: https://stackoverflow.com/a/21912744
def ordered_load(stream):
    assert yaml is not None

    class OrderedLoader(yaml.Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return OrderedDict(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)


def ordered_dump(data, stream=None, Dumper=None, **kwds):
    assert yaml is not None

    Dumper = yaml.Dumper if Dumper is None else Dumper

    class OrderedDumper(Dumper):
        pass

    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items())
    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)
