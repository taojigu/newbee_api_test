from threading import activeCount

import pytest
import requests

from util.const.request_constant import RequestConstant
from util.exception.bad_response_exception import BadResponseException
from util.exception.failed_api_exception import FailedApiException
from util.encrypt import Encrypt
from util.request.vue_api_client import VueAPIClient


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
def login_session(mall_login_param,vue3_anonymous_client):
    result = vue3_anonymous_client.post(RequestConstant.MallUserLoginPath,data=mall_login_param)
    token = result.get(RequestConstant.DataKey)
    assert token is not None
    return {"token":token}


@pytest.fixture(scope="session")
def vue3_client(api_base_url,login_session):


    default_headers = {
        "Content-Type": "application/json",
        **login_session
    }

    return VueAPIClient(base_url=api_base_url, headers=default_headers)


@pytest.fixture(scope="session")
def vue3_anonymous_client(api_base_url):
    default_headers = {
        "Content-Type": "application/json",
    }
    return VueAPIClient(base_url=api_base_url, headers=default_headers)



