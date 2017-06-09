# -*- coding:utf-8 -*-

import os
import json
import click
from hub.hub import Hub

CONFIG_PATH = os.path.expanduser('~') + '/'
CONFIG_NAME = '.tentacle.json'
CONFIG = CONFIG_PATH + CONFIG_NAME
CTX = {}


@click.group(chain=True)
def cli():
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


if __name__ == '__main__':
    cli()
