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

    def search(self, token, query, page=1, page_size=15):
        '''
        :param query: A keyword for querying repositories
        :type query: str
        :param token: The access token of user.It is required.
        :type token: str
        :param page: Current page that starts with one.
        :type page: The number of records that will be displayed on every page.
        :rtype: dict

        Return a dict that includes a list of repositories,
        the count of query, the url of next page, and the url of
        previous page.For example:
        {
            "count": 18497,
            "next": "https://hub.docker.com/v2/search/repositories/?query=nginx&page=2&page_size=2",
            "previous": null,
            "results": [
                {
                    "star_count": 6157,
                    "pull_count": 671232837,
                    "repo_owner": null,
                    "short_description": "Official build of Nginx.",
                    "is_automated": false,
                    "is_official": true,
                    "repo_name": "nginx"
                },
                {
                    "star_count": 7,
                    "pull_count": 51778,
                    "repo_owner": null,
                    "short_description": "Nginx container",
                    "is_automated": true,
                    "is_official": false,
                    "repo_name": "webdevops/nginx"
                }
            ]
        }
        '''
        path = '/v2/search/repositories/'
        params = {
            'query': query,
            'page': page,
            'page_size': page_size
        }
        result = self.get(path, params=params)
        result.raise_for_status()
        return result.json()



