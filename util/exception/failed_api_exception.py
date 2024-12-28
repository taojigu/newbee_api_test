
class FailedApiException(Exception):
    """
    请求接口，返回非逻辑错误，抛出此异常，例errorCode:500
    """

    def __init__(self, response):
        super().__init__()
        self.response = response
        
    def __str__(self):
        # str = super(FailedApiException, self).__str__()
        json = self.response.json()
        code = json.get('code')
        msg = json.get('message')
        request = self.response.request
        url = request.url
        headers = self.response.headers
        trace_id = headers.get("TRACE-ID") or ""
        except_message = " {} : {}:{} request failed, trace-id:{},header:{} body:{}".format(self.response.url, code, msg,trace_id,request.header,request.body)

        except_message = f"{url} request failed; errorCode:{code} message:{msg}, trace-id:{trace_id}"
        return except_message


