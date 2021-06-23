import threading, socket, app, json

IP = '127.0.0.1'
PORT = 5000

s = socket.socket()
s.connect((IP, PORT))

#############################################
# data transform from socket to websocket #

headers = """\
POST /login HTTP/1.1\r
Content-Type: {content_type}\r
Content-Length: {content_length}\r
Host: {host}\r
Connection: close\r
\r\n"""

body = 'username=dor&password=123'
body_bytes = body.encode()
header_bytes = headers.format(
    content_type="application/x-www-form-urlencoded",
    content_length=len(body_bytes),
    host=str(IP) + ":" + str(PORT)
).encode('iso-8859-1')

payload = header_bytes + body_bytes

s.sendall(payload)