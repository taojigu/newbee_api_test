import pytest
from util.encrypt import Encrypt
from util.exception.failed_api_exception import FailedApiException


def test_get_user_inf(vue3_client):
    result = vue3_client.get("api/v1/user/info")
    assert result["nickName"] is not None


def test_user_login_invalid_password(vue3_client,mall_login_param):
    params = mall_login_param.copy()
    fake_password = "fakePassword"
    params["passwordMd5"] = Encrypt.md5_encrypt(fake_password)
    _failed_login_request(vue3_client,params)


@pytest.mark.parametrize("login_name,md5_password,expected_result_code",[
    ("","",510),
    ({},Encrypt.md5_encrypt("fakePassword"),500),
    ("user_name",210,500),
])
def test_user_login_empty_login_name(vue3_client,login_name,md5_password,expected_result_code):
    login_params ={
        "loginName":login_name,
        "passwordMd5": md5_password
    }
    _failed_login_request(vue3_client,login_params,expected_result_code=expected_result_code)

def _failed_login_request(client,login_data,expected_result_code=500):
    with pytest.raises(FailedApiException) as except_info:
        client.post("api/v1/user/login",data=login_data)
    expt = except_info.value
    response = expt.response
    result = response.json()
    result_code = result.get("resultCode")
    assert result_code == expected_result_code




    return


def test_sample():
    assert 1 == 1