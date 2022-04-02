from multiprocessing.pool import ThreadPool

import requests

from http_callback_server import CallbackRequestHandler, CallbackServer


class TestHTTPCallbackServer:
    def get_aysnc_request(self, server: CallbackServer):
        pool = ThreadPool(processes=1)
        return pool.apply_async(server.get_callback_request)

    def test_get_response(self):
        server = CallbackServer(1234)
        callback_url = server.callback_url

        async_request = self.get_aysnc_request(server)
        response = requests.get(callback_url)

        assert response.status_code == 200

        request = async_request.get()
        assert request.url == callback_url

    def test_get_response_with_custom_handler(self):
        class CustomRequestHandler(CallbackRequestHandler):
            def get_status_code(self) -> int:
                return 418

            def get_response_body(self) -> str:
                return "Custom response"

            def get_headers(self) -> dict[str, str]:
                return {"X-Custom-Header": "Custom header"}

            def is_request_valid(self) -> bool:
                params = self.current_request.params
                return params.get("counter") == "2"

        server = CallbackServer(1234, request_handler=CustomRequestHandler)
        callback_url = server.callback_url

        async_request = self.get_aysnc_request(server)

        for i in [1, 2]:
            response = requests.get(callback_url, {"counter": i})
            assert response.status_code == 418
            assert response.text == "Custom response"
            assert response.headers["X-Custom-Header"] == "Custom header"

        request = async_request.get()
        assert request.url == callback_url + "?counter=2"
