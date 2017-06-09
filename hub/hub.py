# -*- coding:utf-8 -*-

from .base_client import BaseClient


class Hub(BaseClient):
    def __init__(self):
        super(Hub, self).__init__('https://hub.docker.com')

    def login(self, username, password):
        '''
        :param username: The name of user on docker hub.
        :type username: str
        :param password: Password of docker hub
        :type password: str
        :rtype: dict

        Returns a dict that includes a valid access token such as:
        {"token": "eyJ4NWMiOls.iTUlJQytE.Q0NBc"}
        '''
        path = '/v2/users/login'
        result = self.post(path, data={
            'username': username,
            'password': password
        })
        result.raise_for_status()
        return result.json()

    



