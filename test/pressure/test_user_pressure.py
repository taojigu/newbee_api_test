from concurrent.futures.thread import ThreadPoolExecutor

from util.const.request_constant import RequestConstant
import pytest


@pytest.mark.parametrize("request_number, max_response_time", [
    (10, 1),
    (20, 1)]
)
def test_userinfo_pressure(vue3_client,request_number,ave_response_time):
    def get_userinfo_request():
        response = vue3_client.get(RequestConstant.MallUserInfoPath)
        response_time = response.elapsed.total_seconds()
        assert response.status_code == 200
        assert response_time < ave_response_time*1.1
        return response_time

    response_time_list = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        for _ in range(request_number):
            future = executor.submit(get_userinfo_request)
            response_time_list.append(future.result())
    av_time = sum(response_time_list)/len(response_time_list)
    assert av_time < ave_response_time
