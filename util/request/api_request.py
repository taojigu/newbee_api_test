import time
import requests
import threading
import logging

from util.exception.bad_response_exception import BadResponseException
from util.exception.failed_api_exception import FailedApiException


class ApiRequest(object):
    """
    请求基础类，App和Web的请求类，都是基于此类
    """
    _instance_lock = threading.Lock()

    def __init__(self):
        self.base_url = None
        self._extra_headers_callback = None


    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(ApiRequest, "_instance"):
            with ApiRequest._instance_lock:
                if not hasattr(ApiRequest, "_instance"):
                    ApiRequest._instance = ApiRequest(*args, **kwargs)
        return ApiRequest._instance

    @property
    def default_headers(self):
        return {'Content-Type': 'application/json',
                "accept": "application/json"}

    def final_headers(self):
        headers = self.default_headers
        if self.extra_headers_callback:
            headers.update(self.extra_headers_callback(headers))
        return headers

    @property
    def extra_headers_callback(self):
        return self._extra_header_callback

    def extra_headers_callback(self, func):
        if func is None:
            return
        self._extra_headers_callback = func

    def get(self, path, query_param=None):
        if query_param is None:
            query_param = {}
        url = self.base_url + path
        header = self.final_headers()
        response = requests.get(url, query_param, headers=header)
        return self._process_response(response)

    def post(self, path, body=None):
        if body is None:
            body = {}
        url = self.base_url + path
        response = requests.post(url, json=body, headers=self.final_headers())
        return self._process_response(response)

    @staticmethod
    def _process_response(response):
        if response.status_code != 200:
            raise BadResponseException(response)

        json = response.json()
        code = json.get('code')
        if code != 200:
            raise FailedApiException(response)
        return json.get('result')
