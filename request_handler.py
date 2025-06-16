from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sqlite3


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
        if self.path == "/register":
            self.handle_register()
        elif self.path == "/login":
            self.handle_login()
        else:
            self.send_error(404, "Not Found")

    def handle_register(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        new_user = json.loads(post_data)

        with sqlite3.connect("db.sqlite3") as conn:
            db_cursor = conn.cursor()

            db_cursor.execute(
                """
                INSERT INTO Users (
                    first_name, last_name, email, bio,
                    username, password, profile_image_url,
                    created_on, active
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, date('now'), 1)
            """,
                (
                    new_user["first_name"],
                    new_user["last_name"],
                    new_user["email"],
                    new_user.get("bio", ""),
                    new_user["username"],
                    new_user["password"],
                    new_user.get("profile_image_url", ""),
                ),
            )

            user_id = db_cursor.lastrowid

        self.send_response(201)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        # ✅ This structure matches frontend expectations
        response = {"valid": True, "token": f"rare_token_user_{user_id}"}
        self.wfile.write(json.dumps(response).encode())

    def handle_login(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        credentials = json.loads(post_data)

        if "username" not in credentials or "password" not in credentials:
            self.send_error(400, "Missing username or password")
            return

        with sqlite3.connect("db.sqlite3") as conn:
            db_cursor = conn.cursor()
            db_cursor.execute(
                """
                SELECT id FROM Users
                WHERE username = ? AND password = ?
            """,
                (credentials["username"], credentials["password"]),
            )
            user = db_cursor.fetchone()

        if user:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            # ✅ Send token + valid flag so frontend works
            response = {"valid": True, "token": f"rare_token_user_{user[0]}"}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            response = {"valid": False}
            self.wfile.write(json.dumps(response).encode())


def main():
    host = ""
    port = 8088
    server = HTTPServer((host, port), RequestHandler)
    print(f"🐍 Rare API Server running on http://localhost:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
