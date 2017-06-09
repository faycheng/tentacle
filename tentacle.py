# -*- coding:utf-8 -*-

import os
import json
import click
from terminaltables import GithubFlavoredMarkdownTable as Table
from hub.hub import Hub

CONFIG_PATH = os.path.expanduser('~') + '/'
CONFIG_NAME = '.tentacle.json'
CONFIG = CONFIG_PATH + CONFIG_NAME
CTX = {}


def pretty_table(data, filters=None, locations=None):
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
            json.dump({
                'auth': {
                    'username': None,
                    'password': None,
                    'token': None
                }
            }, fd, indent=4)
    with open(CONFIG, 'r') as fd:
        config = json.load(fd)
    CTX['username'] = config['auth']['username']
    CTX['password'] = config['auth']['password']
    CTX['token'] = config['auth']['token']


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
    click.echo('Login Success')


@cli.command()
@click.argument('query', type=str)
def search(query):
    res = Hub().search(CTX['token'], query)
    click.echo('Count:{}'.format(res['count']))
    click.echo(
        pretty_table(
            res['results'], filters=[
                'repo_owner', 'short_description'], locations=[
                'repo_name', 'pull_count']))


if __name__ == '__main__':
    cli()
