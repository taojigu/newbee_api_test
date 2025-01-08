import sys
import pytest
from pytest_benchmark.plugin import benchmark
from util.const.request_constant import RequestConstant
import requests

@pytest.mark.skipif(sys.gettrace() is not None, reason="Skipping benchmark during debugging")
def test_user_performance_userinfo(vue3_client, benchmark):

    def user_info_request():
        response = vue3_client.get(RequestConstant.MallUserInfoPath)
        response_time = response.elapsed.total_seconds()
        assert response_time < 1
        return response
    benchmark(user_info_request)
