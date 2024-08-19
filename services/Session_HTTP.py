import datetime

from services.Session import SessionBase


http_ok = b'HTTP/1.1 200 OK\r\n\r\n'
http_404 = b'HTTP/1.1 404 Not Found\r\n\r\n'


def create_http_response(headers, body):
    body_bytes = body.encode('utf-8')

    headers['Content-Length'] = str(len(body_bytes))

    current_time = datetime.datetime.now(datetime.UTC).strftime('%a, %d %b %Y %H:%M:%S GMT')
    headers['Date'] = current_time

    response_lines = [f"HTTP/1.1 200 OK"]
    for key, value in headers.items():
        response_lines.append(f"{key}: {value}")

    response_text = "\r\n".join(response_lines) + "\r\n\r\n" + body
    response_bytes = response_text.encode('utf-8')

    return response_bytes


headers = {
    "Connection": "Keep-Alive",
    "Content-Type": "text/html; charset=UTF-8",
}

body = """<html>
    <head>
        <title>Hi</title>
    </head>
    <body>
    <p>The admin password is 'admin123'</p>
    <p>The admin login is under /secret_login.php</p>
        <br />
    </body>
</html>"""

class SessionHTTP(SessionBase):

    def read_from_socket(self):
        msg = self._read_from_socket()
        if msg is None:
            return False

        if b'GET' in msg:
            if b'favicon.ico' in msg:
                self.message_queue = http_404
            else:
                self.message_queue = create_http_response(headers, body)

        elif b'POST' in msg:
            self.message_queue = http_ok

        return True