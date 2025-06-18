from http.server import BaseHTTPRequestHandler, HTTPServer
from enum import Enum
import json
from models.user import create_user, login_user
from views.tagsView import handle_create_tag, handle_get_tags
from views.post import (
    handle_create_post,
    handle_get_post,
    handle_update_post,
    handle_get_all_posts,
    handle_delete_post,
)


class RequestHandler(BaseHTTPRequestHandler):

    def parse_url(self, path):
        parts = path.strip("/").split("/")
        result = {"resource": parts[0]}

        if len(parts) > 1:
            try:
                result["id"] = int(parts[1])
            except ValueError:
                result["id"] = None

        return result

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header(
            "Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS"
        )
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        body = json.loads(post_data)

        if self.path == "/register":
            self._handle_register(body)
        elif self.path == "/login":
            self._handle_login(body)
        elif self.path == "/posts":
            # 🔐 Grab the token from the headers: "Token rare_token_user_6"
            auth_header = self.headers.get("Authorization")
            if auth_header and auth_header.startswith("Token rare_token_user_"):
                try:
                    user_id = int(auth_header.split("_")[-1])
                    body["user_id"] = user_id
                except ValueError:
                    return self._send_response(400, {"error": "Invalid token format"})
            else:
                return self._send_response(
                    401, {"error": "Authorization header missing or malformed"}
                )

            status, result = handle_create_post(body)
            self._send_response(status, result)
        elif self.path == "/tags" or self.path == "/tags/":
            status, result = handle_create_tag(body)
            self._send_response(status, result)

    def do_GET(self):
        print("🔥 GET hit:", self.path)  # debug print

        if self.path.startswith("/posts/"):
            try:
                post_id = int(self.path.split("/")[-1])
                post = handle_get_post(post_id)

                if post:
                    self._send_response(200, post)
                else:
                    self._send_response(404, {"error": "Post not found"})

            except ValueError:
                self._send_response(400, {"error": "Invalid post ID"})
        elif self.path.rstrip("/") == "/posts":
            status, result = handle_get_all_posts()
            self._send_response(status, result)
        elif self.path.rstrip("/") == "/tags":
            status, result = handle_get_tags()
            self._send_response(status, result)
        else:
            self._send_response(404, {"error": "Route not handled"})

    def do_DELETE(self):
        url = self.parse_url(self.path)
        resource = url["resource"]
        pk = url.get("id", None)

        if resource == "posts" and pk is not None:
            status, _ = handle_delete_post(pk)
            self._send_response(status, {})  # Use your unified response function
        else:
            self._send_response(404, {"error": "Post not found"})

    # 🔐 Register handler with duplicate username/email check
    def _handle_register(self, body):
        result = create_user(body)

        if "error" in result:
            self._send_response(400, {"error": result["error"]})
        else:
            self._send_response(
                201, {"valid": True, "token": f"rare_token_user_{result['id']}"}
            )

    def do_PUT(self):
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)
        data = json.loads(body)

        if self.path.startswith("/posts/"):
            try:
                post_id = int(self.path.split("/")[-1])
                handle_update_post(post_id, data)
                self._send_response(204, {})
            except ValueError:
                self._send_response(400, {"error": "Invalid post ID"})

    # 🔐 Login handler
    def _handle_login(self, body):
        result = login_user(body)
        self._send_response(200, result)

    # 🔁 Shared response helper
    def _send_response(self, status_code, response_obj):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
        self.wfile.write(json.dumps(response_obj).encode())
