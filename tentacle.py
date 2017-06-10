# -*- coding:utf-8 -*-

import os
import sys
import json
import copy
import click
from operator import itemgetter
from terminaltables import GithubFlavoredMarkdownTable as Table
from hub.hub import Hub

CONFIG_PATH = os.path.expanduser('~') + '/'
CONFIG_NAME = '.tentacle.json'
CONFIG = CONFIG_PATH + CONFIG_NAME
CTX = {}


DEFAULT_CONFIG = {
    'auth': {
        'username': None,
        'password': None,
        'token': None
    },
    'table': {
        'search': {
            'filters': ['repo_owner', 'short_description'],
            'locations': ['repo_name', 'pull_count'],
            'sort': {
                'keys': ['pull_count', 'star_count'],
                'reverse': True
            }
        },
        'tag': {
            'filters': ['images', 'creator', 'repository', 'last_updater', 'image_id'],
            'locations': ['name', 'id', 'full_size', 'v2', 'last_updated'],
            'sort': {
                'keys': ['name'],
                'reverse': True
            }
        },
    }
}


def pretty_table(
        data,
        filters=None,
        locations=None,
        sort_keys=None,
        sort_reverse=False):
    headers = []
    for item in data:
        keys = list(item.keys())
        headers = list(set(headers + keys))
    if filters is not None:
        assert isinstance(filters, list)
        headers = [header for header in headers if header not in filters]
    if locations is not None:
        assert isinstance(locations, list)
        valid_locations = [
            location for location in locations if location in headers]
        headers_with_location = valid_locations
        headers_with_location.extend(
            [header for header in headers if header not in valid_locations])
        headers = headers_with_location

    rows = []
    for item in data:
        assert isinstance(item, dict)
        row = []
        for header in headers:
            row.append(item.get(header, ''))
        rows.append(row)
    if sort_keys is not None:
        assert isinstance(sort_keys, list)
        indexs = [headers.index(key) for key in sort_keys if key in headers]
        rows.sort(key=itemgetter(*indexs), reverse=sort_reverse)
    table_data = list()
    table_data.append(headers)
    table_data.extend(rows)
    table = Table(table_data)
    return table.table


@click.group(chain=True)
def cli():
    global CTX
    if not os.path.exists(CONFIG):
        with open(CONFIG, 'w') as fd:
            json.dump(DEFAULT_CONFIG, fd, indent=4)
    with open(CONFIG, 'r') as fd:
        config = json.load(fd)
    CTX['config'] = config


@cli.command()
def login():
    username = click.prompt('Username', type=str)
    password = click.prompt('Password', type=str)
    token = Hub().login(username, password)['token']

    with open(CONFIG, 'r+') as fd:
        config = json.load(fd)
        config['auth'] = {
            'username': username,
            'password': password,
            'token': token
        }
        fd.seek(0)
        json.dump(config, fd, indent=4)
    click.echo('Login success')


@cli.command()
@click.option(
    '--remain_auth',
    type=bool,
    default=False,
    help='Remain the detailed information of authorization if this arguments is true. The default '
    'is false.')
def reset(remain_auth):
    assert os.path.exists(CONFIG)
    click.echo('Remain Auth:{}'.format(remain_auth))
    if remain_auth is False:
        os.remove(CONFIG)
        with open(CONFIG, 'w') as fd:
            json.dump(DEFAULT_CONFIG, fd, indent=4)
        click.echo('Reset config success')
        sys.exit(0)
    with open(CONFIG, 'r+') as fd:
        config = json.load(fd)
        default_config = copy.deepcopy(DEFAULT_CONFIG)
        default_config['auth'] = config['auth']
        fd.seek(0)
        json.dump(default_config, fd, indent=4)
    click.echo('Reset config success')


@cli.command()
@click.argument('query', type=str)
def search(query):
    if CTX['config']['auth']['token'] is None:
        click.echo('Please login with username and password: tentacle login')
        sys.exit(1)
    res = Hub().search(CTX['config']['auth']['token'], query)
    click.echo('Count:{}'.format(res['count']))
    click.echo(
        pretty_table(
            res['results'],
            filters=CTX['config']['table']['search']['filters'],
            locations=CTX['config']['table']['search']['locations'],
            sort_keys=CTX['config']['table']['search']['sort']['keys'],
            sort_reverse=CTX['config']['table']['search']['sort']['reverse'],
        ),
    )


@cli.command()
@click.argument('query', type=str)
def search(query):
    if CTX['config']['auth']['token'] is None:
        click.echo('Please login with username and password: tentacle login')
        sys.exit(1)
    res = Hub().search(CTX['config']['auth']['token'], query)
    click.echo('Count:{}'.format(res['count']))
    click.echo(
        pretty_table(
            res['results'],
            filters=CTX['config']['table']['search']['filters'],
            locations=CTX['config']['table']['search']['locations'],
            sort_keys=CTX['config']['table']['search']['sort']['keys'],
            sort_reverse=CTX['config']['table']['search']['sort']['reverse'],
        ),
    )


@cli.command()
@click.argument('repo', type=str)
def tag(repo):
    res = Hub().tag(repo, CTX['config']['auth']['token'])
    click.echo('Count:{}'.format(res['count']))
    click.echo(
        pretty_table(
            res['results'],
            filters=CTX['config']['table']['tag']['filters'],
            locations=CTX['config']['table']['tag']['locations'],
            sort_keys=CTX['config']['table']['tag']['sort']['keys'],
            sort_reverse=CTX['config']['table']['tag']['sort']['reverse'],
        ),
    )


if __name__ == '__main__':
    cli()
