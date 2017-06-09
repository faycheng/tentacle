# -*- coding:utf-8 -*-
from __future__ import unicode_literals
import json
import logging

import requests


LOG = logging.getLogger(__name__)


class BaseClient(requests.Session):
    def __init__(self, end_point, headers=None):
        super(BaseClient, self).__init__()
        self._end_point = end_point
        self.headers = headers or dict()
        self.headers.update({'Accept': 'application/json',
                             'Content-Type': 'application/json'})
        self.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))

    def build_url(self, path):
        return self._end_point + path

    def get(self, path, **kwargs):
        url = self.build_url(path)
        LOG.debug('{method}\t{url}'.format(method='GET', url=url))
        return super(BaseClient, self).get(url, **kwargs)

    def post(self, path, data=None, **kwargs):
        url = self.build_url(path)
        if data:
            data = json.dumps(data)
        LOG.debug(
            '{method}\t{url}\t{data}'.format(
                method='POST',
                url=url,
                data=data))
        return super(BaseClient, self).post(url, data, **kwargs)

    def delete(self, path, **kwargs):
        url = self.build_url(path)
        LOG.debug('{method}\t{url}'.format(method='DELETE', url=url))
        return super(BaseClient, self).delete(url, **kwargs)

