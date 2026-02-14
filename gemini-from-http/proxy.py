#!/usr/bin/env python3
import argparse
import logging
import os
import pathlib
import ssl
import socketserver
import urllib.parse
import urllib.request


context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
proxied_hosts = []

class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        with context.wrap_socket(self.request, server_side=True) as sock:
            recv = sock.recv(1024)
            recv = recv.decode("ASCII")
            assert recv.endswith("\r\n"), f"Received request {repr(recv)} that does not end in \\r\\n"
            absolute_uri = recv.removesuffix("\r\n")
            assert absolute_uri.startswith("gemini://"), f"Request for uri {absolute_uri} does not start with gemini://"
            logging.info(absolute_uri)
            absolute_uri = urllib.parse.urlparse(absolute_uri)
            host = absolute_uri.netloc

            global proxied_hosts
            assert host in proxied_hosts, f"{host} not in {proxied_hosts}"
            request = urllib.request.Request(absolute_uri._replace(scheme="https").geturl(), headers={"Host": host})
            request.add_header("Accept", "text/gemini")
            with urllib.request.urlopen(request) as f:
                content = f.read().decode("UTF8")
            response = "20 text/gemini\r\n"
            response += content

            sock.sendall(response.encode("UTF8"))


def main():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(message)s")
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=1965)
    parser.add_argument("proxied_host", nargs="+")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--certificates-from-path", type=pathlib.Path)
    group.add_argument("--certificates-from-credential")
    args = parser.parse_args()

    if args.certificates_from_path:
        def domain_to_path(server_name):
            domain_path = args.certificates_from_path / server_name
            return  (domain_path / "pubcert.pem" , domain_path / "privkey.pem")

    if args.certificates_from_credential:
        def domain_to_path(server_name):
            credentials_directory = pathlib.Path(os.environ["CREDENTIALS_DIRECTORY"])
            return (credentials_directory / f"{args.certificates_from_credential}_{server_name}_pubcert.pem", credentials_directory / f"{args.certificates_from_credential}_{server_name}_privkey.pem")

    def sni_callback(socket: ssl.SSLSocket, server_name, _context):
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        certfile, keyfile = domain_to_path(server_name)
        context.load_cert_chain(certfile, keyfile)
        socket.context = context

    context.sni_callback = sni_callback

    global proxied_hosts
    proxied_hosts = args.proxied_host

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((args.host, args.port), Handler) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
