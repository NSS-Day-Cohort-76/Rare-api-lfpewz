import json
import sqlite3
from datetime import datetime

def create_post(body):
    required_fields = ["title", "content", "category_id", "user_id"]
    for field in required_fields:
        if field not in body:
            return 400, {"error": f"Missing field: {field}"}

    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
            INSERT INTO Posts (title, content, category_id, user_id, publication_date)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                body["title"],
                body["content"],
                body["category_id"],
                body["user_id"],
                datetime.now().isoformat()
            ),
        )
        post_id = db_cursor.lastrowid

    return 201, {"id": post_id, "message": "Post created"}

# def create_post(post):
#     """
#     Adds a new post to the Posts table.

#     Args:
#         post (dict): The post data from the frontend.

#     Returns:
#         dict: The newly created post as a dictionary
#     """
#     publication_date = datetime.now().isoformat()
#     image_url = post.get("image_url", "")  # Optional

#     with sqlite3.connect("./db.sqlite3") as conn:
#         db_cursor = conn.cursor()

#         db_cursor.execute(
#             """
#             INSERT INTO Posts (
#                 user_id,
#                 category_id,
#                 title,
#                 content,
#                 image_url,
#                 publication_date,
#                 approved
#             )
#             VALUES (?, ?, ?, ?, ?, ?, false)
#         """,
#             (
#                 post["user_id"],
#                 post["category_id"],
#                 post["title"],
#                 post["content"],
#                 image_url,
#                 publication_date,
#             ),
#         )

#         new_post_id = db_cursor.lastrowid

    # Return the full post object
    return {
        "id": new_post_id,
        "user_id": post["user_id"],
        "category_id": post["category_id"],
        "title": post["title"],
        "content": post["content"],
        "image_url": image_url,
        "publication_date": publication_date,
        "approved": True
    }


def get_all_posts():
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
        """
        )

        posts = []
        dataset = db_cursor.fetchall()
        for row in dataset:

            user = {
                "id": row["user_id"],
                "firstName": row["user_first_name"],
                "lastName": row["user_last_name"]
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


def delete_post(post_id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("DELETE FROM Posts WHERE id = ?", (post_id,))


# def get_all_posts():
#     with sqlite3.connect("./db.sqlite3") as conn:
#         conn.row_factory = sqlite3.Row
#         db_cursor = conn.cursor()

#         db_cursor.execute(
#             """
#             SELECT
#                 p.id,
#                 p.category_id,
#                 p.user_id,
#                 c.label AS category_label,
#                 u.first_name AS user_first_name,
#                 u.last_name AS user_last_name
#             FROM "Posts" p
#             JOIN Category c ON c.id = p.category_id
#             JOIN User u ON u.id = p.user_id
#             """
#         )

#         query_results = db_cursor.fetchall()
#         posts = []
#         for row in query_results:
#             category = {
#                 "id": row["category_id"],
#                 "label": row["category_label"],
#             }
#             user = {
#                 "id": row["user_id"],
#                 "first_name": row["user_first_name"],
#                 "last_name": row["user_last_name"],
#             }
#             post = {
#                 "id": row["id"],
#                 "category_id": row["category_id"],
#                 "category": category,
#                 "user_id": row["user_id"],
#                 "user": user,
#                 # "created_at": row["created_at"] if row["created_at"] is not None else ""
#             }
#             posts.append(post)
#     return posts
