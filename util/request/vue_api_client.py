import requests

from util.exception.bad_response_exception import BadResponseException
from util.exception.failed_api_exception import FailedApiException


class VueAPIClient:
    """
    A simple Vue3 API client class to encapsulate base URL and headers.
    """

    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    def get(self, endpoint, headers=None, params=None):
        merged_headers = {**self.headers, **(headers or {})}
        response = requests.get(f"{self.base_url}{endpoint}", headers=merged_headers, params=params)
        return self._process_response(response)

    def post(self, endpoint, data=None, headers=None, params=None):
        merged_headers = {**self.headers, **(headers or {})}
        response = requests.post(f"{self.base_url}{endpoint}", json=data, headers=merged_headers, params=params)
        return self._process_response(response)

    @staticmethod
    def _process_response(response):
        if response.status_code != 200:
            raise BadResponseException(response)

        json = response.json()
        result_code = json.get('resultCode')
        if result_code != 200:
            raise FailedApiException(response)
        return response