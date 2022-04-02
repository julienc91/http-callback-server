from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qsl, urlparse

from requests import Request


def build_request_from_request_handler(
    request_handler: BaseHTTPRequestHandler,
) -> Request:
    host, port = request_handler.server.server_address
    parsed_url = urlparse(request_handler.path)
    return Request(
        method=request_handler.command,
        url=f"http://{host}:{port}{request_handler.path}",
        headers=dict(request_handler.headers),
        params=dict(parse_qsl(parsed_url.query)),
    )
