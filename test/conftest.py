
import pytest
import requests
from urllib3 import request

from util.encrypt import Encrypt

@pytest.fixture(scope="session")
def base_url():
    return "http://backend-api-01.newbee.ltd/"

@pytest.fixture(scope="session")
def header():
    return {"Content-Type":"application/json"}

@pytest.fixture(scope="session")
def mall_login_param():
    login_name = "18810321945"
    password = "123456"
    md5_password = Encrypt.md5_encrypt(password)
    return {
        "loginName": login_name,
        "passwordMd5":md5_password
    }


@pytest.fixture(scope="session")
def login_session(mall_login_param,base_url):
    url = f'{base_url}/api/v1/user/login'
    response = requests.post(url,json=login_session)
    assert response.status_code == 200
    token = response.json().get("data")
    return {"token":token}