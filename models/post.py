import sqlite3
from datetime import datetime


def create_post(body):
    required_fields = ["title", "content", "category_id", "user_id"]
    for field in required_fields:
        if field not in body:
            return 400, {"error": f"Missing field: {field}"}

    # 🧠 Look up is_staff
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("SELECT is_staff FROM Users WHERE id = ?", (body["user_id"],))
        row = db_cursor.fetchone()
        is_staff = row[0] if row else 0

    approved = 1 if is_staff else 0

    # 💾 Insert post with approved status
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
            INSERT INTO Posts (
                title, content, category_id, user_id, publication_date, image_url, approved
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                body["title"],
                body["content"],
                body["category_id"],
                body["user_id"],
                datetime.now().isoformat(),
                body.get("image_url", ""),  # fallback if missing
                approved,
            ),
        )
        post_id = db_cursor.lastrowid

    return 201, {"id": post_id, "message": "Post created"}


def get_all_posts(requesting_user_id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Step 1: Get the user's is_staff value
        db_cursor.execute(
            "SELECT is_staff FROM Users WHERE id = ?", (requesting_user_id,)
        )
        row = db_cursor.fetchone()
        is_staff = row[0] if row else 0

        # Step 2: Build base query
        query = """
            SELECT
                p.id, p.title, p.content, p.image_url, p.publication_date,
                p.user_id, p.approved,
                u.username, u.first_name AS user_first_name, u.last_name AS user_last_name,
                c.id AS category_id, c.label AS category_label
            FROM Posts p
            JOIN Users u ON p.user_id = u.id
            JOIN Categories c ON p.category_id = c.id
        """

        # Step 3: Add filter if not staff
        if not is_staff:
            query += " WHERE p.approved = 1"

        db_cursor.execute(query)
        dataset = db_cursor.fetchall()

        posts = []
        for row in dataset:
            posts.append(
                {
                    "id": row["id"],
                    "title": row["title"],
                    "content": row["content"],
                    "image_url": row["image_url"],
                    "publication_date": row["publication_date"],
                    "user_id": row["user_id"],
                    "approved": row["approved"],
                    "user": {
                        "id": row["user_id"],
                        "firstName": row["user_first_name"],
                        "lastName": row["user_last_name"],
                    },
                    "category": {
                        "id": row["category_id"],
                        "label": row["category_label"],
                    },
                    "author": row["username"],
                }
            )

        return posts


def get_single_post(post_id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
            SELECT
                p.id,
                p.title,
                p.content,
                p.image_url,
                p.publication_date,
                p.user_id,
                u.username,
                u.first_name AS user_first_name,
                u.last_name AS user_last_name,
                c.id AS category_id,
                c.label AS category_label
            FROM Posts p
            JOIN Users u ON p.user_id = u.id
            JOIN Categories c ON p.category_id = c.id
            WHERE p.id = ?
            """,
            (post_id,),
        )

        row = db_cursor.fetchone()

        if row:
            user = {
                "id": row["user_id"],
                "firstName": row["user_first_name"],
                "lastName": row["user_last_name"],
            }
            category = {
                "id": row["category_id"],
                "label": row["category_label"],
            }
            post = {
                "id": row["id"],
                "title": row["title"],
                "content": row["content"],
                "image_url": row["image_url"],
                "publication_date": row["publication_date"],
                "user_id": row["user_id"],
                "user": user,
                "category_id": row["category_id"],
                "category": category,
                "author": row["username"],
            }

            return post
        else:
            return None


def delete_post(post_id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("DELETE FROM Posts WHERE id = ?", (post_id,))


def approve_post(post_id, approved_value):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute(
            "UPDATE Posts SET approved = ? WHERE id = ?", (approved_value, post_id)
        )


def get_most_recent_post():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
            SELECT
                p.id,
                p.title,
                p.content,
                p.image_url,
                p.publication_date,
                p.user_id,
                u.username,
                u.first_name AS user_first_name,
                u.last_name AS user_last_name,
                c.id AS category_id,
                c.label AS category_label
            FROM Posts p
            JOIN Users u ON p.user_id = u.id
            JOIN Categories c ON p.category_id = c.id
            ORDER BY p.publication_date DESC
            LIMIT 1
            """
        )
        row = db_cursor.fetchone()
        if row is None:
            return None

        user = {
            "id": row["user_id"],
            "firstName": row["user_first_name"],
            "lastName": row["user_last_name"],
        }
        category = {
            "id": row["category_id"],
            "label": row["category_label"],
        }
        post = {
            "id": row["id"],
            "title": row["title"],
            "content": row["content"],
            "image_url": row["image_url"],
            "publication_date": row["publication_date"],
            "user_id": row["user_id"],
            "user": user,
            "category_id": row["category_id"],
            "category": category,
            "author": row["username"],
        }
        return post


def get_posts_by_category(category_id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT
                p.id,
                p.title,
                p.content,
                p.image_url,
                p.publication_date,
                p.user_id,
                u.username,
                u.first_name AS user_first_name,
                u.last_name AS user_last_name,
                c.id AS category_id,
                c.label AS category_label
            FROM Posts p
            JOIN Users u ON p.user_id = u.id
            JOIN Categories c ON p.category_id = c.id
            WHERE p.category_id = ?
            ORDER BY p.publication_date DESC
            """,
            (category_id,),
        )

        posts = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            user = {
                "id": row["user_id"],
                "firstName": row["user_first_name"],
                "lastName": row["user_last_name"],
            }
            category = {
                "id": row["category_id"],
                "label": row["category_label"],
            }
            post = {
                "id": row["id"],
                "title": row["title"],
                "content": row["content"],
                "image_url": row["image_url"],
                "publication_date": row["publication_date"],
                "user_id": row["user_id"],
                "user": user,
                "category_id": row["category_id"],
                "category": category,
                "author": row["username"],
            }

            posts.append(post)

        return posts
