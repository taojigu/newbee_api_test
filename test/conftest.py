from threading import activeCount

import pytest
import requests

from util.exception.bad_response_exception import BadResponseException
from util.exception.failed_api_exception import FailedApiException
from util.encrypt import Encrypt


def pytest_addoption(parser):
    parser.addoption("--login-name", action="store", default=None, help="login user name of vue client")
    parser.addoption("--password", action="store", default=None, help="password for vue client user")
    parser.addoption("--api-base-url", action="store",default="http://backend-api-01.newbee.ltd/", help=" base url of api")


@pytest.fixture(scope="session")
def api_base_url(request):
    return request.config.getoption("--api-base-url")


@pytest.fixture(scope="session")
def header():
    return {"Content-Type": "application/json"}


@pytest.fixture(scope="session")
def mall_login_param(request):
    login_name = request.config.getoption("--login-name")
    password = request.config.getoption("--password")
    md5_password = Encrypt.md5_encrypt(password)
    return {
        "loginName": login_name,
        "passwordMd5": md5_password
    }


@pytest.fixture(scope="session")
def login_session(mall_login_param, api_base_url):
    url = f'{api_base_url}/api/v1/user/login'
    response = requests.post(url, json=mall_login_param)
    assert response.status_code == 200
    response_json = response.json()
    token = response_json.get("data")
    assert token is not None
    return {"token":token}


@pytest.fixture(scope="session")
def vue3_client(api_base_url,login_session):
    default_headers = {
        "Content-Type": "application/json",
        **login_session
    }

    class VueAPIClient:
        """
        A simple Vue3 API client class to encapsulate base URL and headers.
        """

        def __init__(self, base_url, headers):
            self.base_url = base_url
            self.headers = headers

        def get(self, endpoint, headers=None):
            merged_headers = {**self.headers, **(headers or {})}
            response = requests.get(f"{self.base_url}{endpoint}", headers=merged_headers)
            return self._process_response(response)

        def post(self, endpoint, data=None, headers=None):
            merged_headers = {**self.headers, **(headers or {})}
            response = requests.post(f"{self.base_url}{endpoint}", json=data, headers=merged_headers)
            return self._process_response(response)

        @staticmethod
        def _process_response(response):
            if response.status_code != 200:
                raise BadResponseException(response)

            json = response.json()
            code = json.get('resultCode')
            if code != 200:
                raise FailedApiException(response)
            return json.get('data')

    return VueAPIClient(base_url=api_base_url, headers=default_headers)


