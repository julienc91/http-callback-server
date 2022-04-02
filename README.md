# http-callback-server

Python library to receive an HTTP request in a single line of code.

Compatibility: Python 3.7+

## Quick Start

Open a port and wait for the callback request:

```python
>>> from http_callback_server import CallbackServer
>>> callback_server = CallbackServer(port=8080, host="localhost")
>>> callback_server.callback_url
'http://localhost:8080/'
>>> request = callback_server.get_callback_request()
127.0.0.1 - - [02/Apr/2022 21:20:33] "GET /callback?token=123456 HTTP/1.1" 200 -
>>> request.url
'http://127.0.0.1:8080/callback?token=123456'
>>> request.params
{'token': '123456'}
```
