import socket
import ssl
import sys
import urllib.parse

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

url = sys.argv[1]
split_url = urllib.parse.urlsplit(url)

with socket.create_connection((split_url.netloc, 1965)) as sock:
    with context.wrap_socket(sock, server_hostname=split_url.netloc) as ssock:
        ssock.sendall(url.encode("ascii") + b"\r\n")
        recv = b""
        while True:
            chunk = ssock.recv()
            if not chunk:
                break
            recv += chunk

header, rest = recv.split(b"\r\n", 1)
header = header.decode("utf8")
assert header.startswith("2"), f"Response header {header} is not 2*"

sys.stdout.buffer.write(rest)
