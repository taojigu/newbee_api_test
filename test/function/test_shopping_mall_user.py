import pytest
from faker.proxy import Faker

from util.const.request_constant import RequestConstant
from util.encrypt import Encrypt
from util.exception.failed_api_exception import FailedApiException


def test_get_user_info(vue3_client):
    response = vue3_client.get(RequestConstant.MallUserInfoPath)
    result = response.json()
    result_code = result.get(RequestConstant.ResultCodeKey)
    assert result_code == 200
    data = result.get(RequestConstant.DataKey)
    name = data.get("nickName")
    assert name is not None


def test_user_login_invalid_password(vue3_client, mall_login_param):
    params = mall_login_param.copy()
    fake_password = "fakePassword"
    params["passwordMd5"] = Encrypt.md5_encrypt(fake_password)
    _failed_login_request(vue3_client, params)


@pytest.mark.parametrize("login_name,md5_password,expected_result_code", [
    ("", "", 510),
    ({}, Encrypt.md5_encrypt("fakePassword"), 500),
    ("user_name", 210, 500),
    (1881388177, "", 510)
])
def test_user_login_empty_login_name(vue3_client, login_name, md5_password, expected_result_code):
    login_params = RequestConstant.login_data(login_name,md5_password)
    _failed_login_request(vue3_client, login_params, expected_result_code=expected_result_code)


def _failed_login_request(client, login_data, expected_result_code=500):
    with pytest.raises(FailedApiException) as except_info:
        client.post(RequestConstant.MallUserLoginPath, data=login_data)
    expt = except_info.value
    response = expt.response
    result = response.json()
    result_code = result.get(RequestConstant.ResultCodeKey)
    assert result_code == expected_result_code
    return


def test_register_user(vue3_anonymous_client):
    faker = Faker("zh_CN")
    name = faker.phone_number()
    password = faker.password()
    register_data = {
        RequestConstant.LoginNameKey:name,
        RequestConstant.PasswordKey:password
    }
    response = vue3_anonymous_client.post(RequestConstant.MallUserRegisterPath,data=register_data)
    result = response.json()
    result_code = result.get(RequestConstant.ResultCodeKey)
    assert result_code == 200
    login_data = RequestConstant.login_data(name,Encrypt.md5_encrypt(password))
    response = vue3_anonymous_client.post(RequestConstant.MallUserLoginPath,data=login_data)
    result = response.json()
    result_code = result.get(RequestConstant.ResultCodeKey)
    assert result_code ==200

