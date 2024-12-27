

def test_get_user_inf(vue3_client):
    result = vue3_client.get("api/v1/user/info")
    assert result["nickName"] is not None