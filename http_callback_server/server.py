import threading
from http.server import HTTPServer
from typing import Any, Optional, Type

from requests import Request

from .request_handler import CallbackRequestHandler


class Server(HTTPServer):
    """
    A wrapper around HTTPServer that keeps a reference to the latest incoming request.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.callback_request: Optional[Request] = None

    def set_callback_request(self, request: Request) -> None:
        """
        Set the reference to the latest incoming request.
        :param request: the latest incoming request.
        """
        self.callback_request = request

    def shutdown_after_request(self) -> None:
        """
        Shutdown the server to allow the main process to continue.
        """
        killer = threading.Thread(target=self.shutdown)
        killer.daemon = True
        killer.start()


class CallbackServer:
    """
    This class will open a temporary HTTP server ready to receive a callback request.
    When the callback request is received, the server will be shutdown.
    """

    def __init__(
        self,
        port: int,
        host: str = "",
        request_handler: Type[CallbackRequestHandler] = CallbackRequestHandler,
    ) -> None:
        """
        Initialize the server.
        :param port: port to listen on.
        :param host: host to listen on, default to localhost.
        :param request_handler: the request handler to use.
        """
        self.port = port
        self.host = host or "127.0.0.1"

        self._server = Server((self.host, self.port), request_handler)

    @property
    def callback_url(self) -> str:
        """
        Get the server's callback URL.
        :return: the callback URL.
        """
        return f"http://{self.host}:{self.port}/"

    def get_callback_request(self) -> Optional[Request]:
        """
        Start the server and wait for the callback request.
        :return: the latest callback request.
        """
        self._server.serve_forever()
        return self._server.callback_request
