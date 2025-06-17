from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from models.user import create_user, login_user


class RequestHandler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header(
            "Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS"
        )
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        body = json.loads(post_data)

        if self.path == "/register":
            self._handle_register(body)
        elif self.path == "/login":
            self._handle_login(body)
        else:
            self._send_response(404, {"error": "Endpoint not found"})

    # 🔐 Register handler with duplicate username/email check
    def _handle_register(self, body):
        result = create_user(body)

        if "error" in result:
            self._send_response(400, {"error": result["error"]})
        else:
            self._send_response(
                201, {"valid": True, "token": f"rare_token_user_{result['id']}"}
            )

    # 🔐 Login handler
    def _handle_login(self, body):
        result = login_user(body)
        self._send_response(200, result)

    # 🔁 Shared response helper
    def _send_response(self, status_code, response_obj):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(response_obj).encode())


def main():
    host = ""
    port = 8088
    server = HTTPServer((host, port), RequestHandler)
    print(f"🐍 Rare API Server running on http://localhost:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
