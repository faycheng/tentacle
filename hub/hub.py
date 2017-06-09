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
        :param query: The keyword for querying repositories
        :type query: str
        :param token: The access token of user.It is required.
        :type token: str
        :param page: Current page that starts with one.
        :type page: The number of records that will be displayed on every page.
        :rtype: dict

        Returns a dict that includes a list of repositories,
        the count of query, the url of next page, and the url of
        previous page.
        For example:
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
        headers = {
            'Authorization': "JWT {}".format(token)
        }
        path = '/v2/search/repositories/'
        params = {
            'query': query,
            'page': page,
            'page_size': page_size
        }
        result = self.get(path, params=params, headers=headers)
        result.raise_for_status()
        return result.json()

    def show(self, repo, token=None):
        '''
        :param repo: The name of repository that include namespace and image's name.
        :type repo: str
        :param token: The access token of user.It is optional.Token is required
        if you want to show detailed information of private repository.
        :type token: str
        :rtype: dict
        Returns a dict that includes detailed information of repository.The information
        includes the repository name, the repository type, the repository description,
        the repository permissions, and so on.
        For Example:
        {
            "user": "faycheng",
            "name": "nginx",
            "namespace": "faycheng",
            "repository_type": "image",
            "status": 1,
            "description": "",
            "is_private": false,
            "is_automated": false,
            "can_edit": false,
            "star_count": 0,
            "pull_count": 1,
            "last_updated": "2017-06-08T14:28:30.286399Z",
            "build_on_cloud": null,
            "has_starred": false,
            "full_description": "Dockerfile:\n\nFROM nginx\nMAINTAINER FayCheng <fay.cheng.cn@gmail.com>\n\nENV MYSQL_ROOT_PASSWORD dangerous\nCOPY ./nginx.conf /etc/nginx/nginx.conf\nRUN ln -s /usr/share/nginx/html /html\nWORKDIR /usr/share/nginx/html\n\nUsage:\ndocker run -v ./html:/html -d faycheng/nginx:gzip",
            "affiliation": null,
            "permissions": {
                "read": true,
                "write": false,
                "admin": false
                }
        }
        '''
        path = '/v2/repositories/{}/'.format(repo)
        headers = token or {}
        result = self.get(path, headers=headers)
        result.raise_for_status()
        return result.json()

    def list(self, username, token=None):
        '''
        :param username: The name of user on docker hub.
        :type username: str
        :param token: The access token of user.It is optional.Token is required if you
        want to list all repositories that incloud private repositories and public repositories.
        :type token: str
        :rtype: list[dict]
        Returns a list of repositories on the docker hub.
        For example:
        [
            {
                "namespace": "faycheng", "name": "nginx"
            },
            {
                "namespace": "faycheng", "name": "mysql"
            }
        ]
        '''
        path = '/v2/users/{}/repositories/'.format(username)
        headers = token or {}
        result = self.get(path, headers=headers)
        result.raise_for_status()
        return result.json()

    def tag(self, repo, token=None):
        '''
        :param repo: The name of repository that include namespace and image's name.
        :type repo: str
        :param token: The access token of user.It is optional.Token is required
        if you want to list tags of private repository.
        :type token: str
        :rtype: dict
        Returns a dict that includes a list of tags,
        the count of query, the url of next page, and the url of
        previous page.
        For Example:
        {
           "count":1,
           "next":null,
           "previous":null,
           "results":[
              {
                 "name":"gzip",
                 "full_size":44809657,
                 "images":[
                    {
                       "size":44809657,
                       "architecture":"amd64",
                       "variant":null,
                       "features":null,
                       "os":"linux",
                       "os_version":null,
                       "os_features":null
                    }
                 ],
                 "id":11691555,
                 "repository":1556265,
                 "creator":1516346,
                 "last_updater":1516346,
                 "last_updated":"2017-06-08T14:28:29.762439Z",
                 "image_id":null,
                 "v2":true
              }
           ]
        }
        '''
        path = '/v2/repositories/{}/tags/'.format(repo)
        headers = token or {}
        result = self.get(path, headers=headers)
        result.raise_for_status()
        return result.json()


