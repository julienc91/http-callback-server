import threading
from http.server import HTTPServer
from typing import Any, Optional, Type

from requests import Request

from .request_handler import CallbackRequestHandler


class Server(HTTPServer):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.callback_request: Optional[Request] = None

    def set_callback_request(self, request: Request) -> None:
        self.callback_request = request

    def shutdown_after_request(self) -> None:
        killer = threading.Thread(target=self.shutdown)
        killer.daemon = True
        killer.start()


class CallbackServer:
    def __init__(
        self,
        port: int,
        host: str = "",
        request_handler: Type[CallbackRequestHandler] = CallbackRequestHandler,
    ) -> None:
        self.port = port
        self.host = host or "127.0.0.1"

        self._server = Server((self.host, self.port), request_handler)

    @property
    def callback_url(self) -> str:
        return f"http://{self.host}:{self.port}/"

    def get_callback_request(self) -> Optional[Request]:
        self._server.serve_forever()
        return self._server.callback_request
