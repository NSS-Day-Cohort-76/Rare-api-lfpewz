from http.server import HTTPServer
from request_handler import RequestHandler
from http.server import BaseHTTPRequestHandler, HTTPServer


def main():
    host = ""
    port = 8088
    server = HTTPServer((host, port), RequestHandler)
    print(f"🐍 Rare API Server running on http://localhost:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
