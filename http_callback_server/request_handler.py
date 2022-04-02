from functools import cached_property
from http.server import BaseHTTPRequestHandler
from typing import TYPE_CHECKING

from requests import Request

from .request import build_request_from_request_handler

if TYPE_CHECKING:
    from .server import Server


class CallbackRequestHandler(BaseHTTPRequestHandler):
    """
    A request handler that will initialize the reference for the latest request
    on the server object. It is responsible for building and sending the response.
    """

    server: "Server"

    def do_GET(self) -> None:
        """
        Handle a GET request.
        """
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
        """
        The current request, as a `requests.Request` object.
        :return: the current request.
        """
        return build_request_from_request_handler(self)

    def is_request_valid(self) -> bool:
        """
        Determine if the request is valid. If it is, the reference will be set
        on the server instance.
        :return: a boolean.
        """
        return True

    def should_stop_server_after_request(self) -> bool:
        """
        Determine if the server should stop after the current request.
        :return: a boolean.
        """
        return self.is_request_valid()

    def get_headers(self) -> dict[str, str]:
        """
        Build the headers to send in the response.
        :return: a dictionary.
        """
        return {}

    def get_status_code(self) -> int:
        """
        Set the status code of the response.
        :return: an integer.
        """
        return 200

    def get_response_body(self) -> str:
        """
        Build the body of the response.
        :return: a string.
        """
        return "OK"
