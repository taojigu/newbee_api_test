
class BadResponseException(Exception):
    """
    访问接口，网络异常或者超时抛出此异常
    """

    def __init__(self, response):
        super().__init__()
        self.response = response

    def __str__(self):
        headers = self.response.headers
        trace_id = headers.get("TRACE-ID") or ""
        request = self.response.request
        except_message = " {} : {} request failed:{} trace-id:{} response header:{} request body:{}".format(
            self.response.url, self.response.status_code, self.response.content, trace_id,headers,request.body )

        return except_message
