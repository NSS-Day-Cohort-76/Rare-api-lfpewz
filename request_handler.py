from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs

# 🔼 All imports up top like a pro
from models.user import create_user, login_user
from views.user_view import handle_get_all_users  # ✅ ADD THIS
from views.tagsView import (
    handle_create_tag,
    handle_get_tags,
    handle_delete_tag,
    handle_update_tag,
)
from views.post import (
    handle_create_post,
    handle_get_post,
    handle_update_post,
    handle_get_all_posts,
    handle_delete_post,
    handle_get_most_recent_post,
)

from views.category import (
    handle_get_all_categories,
    handle_create_category,
    handle_delete_category,
    handle_update_category,
)

from views.comment_view import (
    handle_get_comments,
    handle_create_comment,
    handle_update_comment,
    handle_delete_comment,
    handle_get_comment_by_id,
)


class RequestHandler(BaseHTTPRequestHandler):

    def parse_url(self, path):
        path_parts = path.strip("/").split("?")
        resource_path = path_parts[0].split("/")
        query_params = {}

        if len(path_parts) > 1:
            query_params = parse_qs(path_parts[1])

        return {
            "resource": resource_path[0],
            "id": (
                int(resource_path[1])
                if len(resource_path) > 1 and resource_path[1].isdigit()
                else None
            ),
            "query_params": query_params,
        }

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header(
            "Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS"
        )
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_GET(self):
        parsed = self.parse_url(self.path)
        resource = parsed["resource"]
        id = parsed["id"]
        query_params = parsed["query_params"]

        # Special case route (not handled by parse_url)
        if self.path.rstrip("/") == "/posts/mostRecentPost":
            status, result = handle_get_most_recent_post()
            self._send_response(status, result)
            return  # ✅ prevent fallthrough to 404

        if resource == "users":  # ✅ Admin-only user list
            status, result = handle_get_all_users()
            self._send_response(status, result)

        elif resource == "tags":
            status, result = handle_get_tags()
            self._send_response(status, result)

        elif resource == "categories":
            status, result = handle_get_all_categories()
            self._send_response(status, result)

        elif resource == "comments":
            if id is not None:
                status, result = handle_get_comment_by_id(id)
            else:
                status, result = handle_get_comments(resource, query_params)
            self._send_response(status, result)

        elif resource == "posts":
            if id is not None:
                post = handle_get_post(id)
                if post:
                    self._send_response(200, post)
                else:
                    self._send_response(404, {"error": "Post not found"})
            else:
                status, result = handle_get_all_posts()
                self._send_response(status, result)

        else:
            self._send_response(404, {"error": "Route not handled"})

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        body = json.loads(post_data)

        if self.path == "/register":
            self._handle_register(body)

        elif self.path == "/login":
            self._handle_login(body)

        elif self.path == "/tags":
            status, result = handle_create_tag(body)
            self._send_response(status, result)

        elif self.path == "/posts":
            auth_header = self.headers.get("Authorization")
            if auth_header and auth_header.startswith("Token "):
                try:
                    user_id = int(auth_header.split(" ")[1])
                    body["user_id"] = user_id
                except (IndexError, ValueError):
                    return self._send_response(400, {"error": "Invalid token format"})
            else:
                return self._send_response(
                    401, {"error": "Authorization header missing or malformed"}
                )

            status, result = handle_create_post(body)
            self._send_response(status, result)

        elif self.path == "/comments":
            status, result = handle_create_comment(body)
            self._send_response(status, result)

        elif self.path == "/categories" and self.command == "POST":
            status, result = handle_create_category(body)
            self._send_response(status, result)

        else:
            self._send_response(404, {"error": "Route not handled"})

    def do_PUT(self):
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)
        data = json.loads(body)

        parsed = self.parse_url(self.path)
        resource = parsed["resource"]
        id = parsed["id"]

        if resource == "posts" and id is not None:
            handle_update_post(id, data)
            self._send_response(204, {})

        elif resource == "tags" and id is not None:
            status, result = handle_update_tag(id, data)
            self._send_response(status, result)

        elif resource == "comments" and id is not None:
            status, result = handle_update_comment(id, data)
            self._send_response(status, result)

        elif resource == "categories" and id is not None:
            status, result = handle_update_category(id, data)
            self._send_response(status, result)

        elif resource == "users" and id is not None:
            from views.user_view import handle_update_user

            status, result = 204, handle_update_user(id, data)
            self._send_response(status, result)

        else:
            self._send_response(404, {"error": "Route not handled"})

    def do_DELETE(self):
        parsed = self.parse_url(self.path)
        resource = parsed["resource"]
        id = parsed["id"]

        if resource == "tags" and id is not None:
            status, result = handle_delete_tag(id)
            self._send_response(status, result)

        elif resource == "posts" and id is not None:
            status, _ = handle_delete_post(id)
            self._send_response(status, {})

        elif resource == "comments" and id is not None:
            status, result = handle_delete_comment(id)
            self._send_response(status, result if result else {})

        elif resource == "categories" and id is not None:
            status, result = handle_delete_category(id)
            self._send_response(status, result if result else {})

        else:
            self._send_response(404, {"error": "Route not handled"})

    def _handle_register(self, body):
        result = create_user(body)
        if "error" in result:
            self._send_response(400, {"error": result["error"]})
        else:
            self._send_response(
                201,
                {
                    "valid": True,
                    "user_id": result["id"],
                    "isStaff": result.get("isStaff", 1),
                },
            )

    def _handle_login(self, body):
        result = login_user(body)
        self._send_response(200, result)

    def _send_response(self, status_code, response_obj):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
        self.wfile.write(json.dumps(response_obj).encode())
