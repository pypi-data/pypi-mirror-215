import os
import socketserver
from http.server import SimpleHTTPRequestHandler
from typing import List

from http_servers.options import ServerOptions
from http_servers.parser import parse_options


def make_handler_class(options: ServerOptions):
    class CustomRequestHandler(SimpleHTTPRequestHandler):
        def end_headers(self):
            if not options.cache:
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.send_header("Pragma", "no-cache")
                self.send_header("Expires", "0")

            if options.cors:
                self.send_header("Access-Control-Allow-Origin", "*")
            SimpleHTTPRequestHandler.end_headers(self)

    return CustomRequestHandler


def run_server(args: List[str] = None):
    options = parse_options(args)
    handler_class = make_handler_class(options)

    os.chdir(options.source_dir)

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((options.host, options.port), handler_class) as httpd:
        print("serving at port", options.port)
        httpd.serve_forever()
