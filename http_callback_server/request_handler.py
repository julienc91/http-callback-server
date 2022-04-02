from functools import cached_property
from http.server import BaseHTTPRequestHandler
from typing import TYPE_CHECKING

from requests import Request

from .request import build_request_from_request_handler

if TYPE_CHECKING:
    from .server import Server


class CallbackRequestHandler(BaseHTTPRequestHandler):
    server: "Server"

    def do_GET(self) -> None:
        self.send_response(self.get_status_code())
        for key, value in self.get_headers().items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(self.get_response_body().encode())

        if self.is_request_valid():
            self.server.set_callback_request(self.current_request)

        if self.should_stop_server_after_request():
            self.server.shutdown_after_request()

    @cached_property
    def current_request(self) -> Request:
        return build_request_from_request_handler(self)

    def is_request_valid(self) -> bool:
        return True

    def should_stop_server_after_request(self) -> bool:
        return self.is_request_valid()

    def get_headers(self) -> dict[str, str]:
        return {}

    def get_status_code(self) -> int:
        return 200

    def get_response_body(self) -> str:
        return "OK"
