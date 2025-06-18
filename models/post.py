import json
import sqlite3
from datetime import datetime


def create_post(post):
    """
    Adds a new post to the Posts table.

    Args:
        post (dict): The post data from the frontend.

    Returns:
        dict: Contains the ID of the new post like { "id": 3 }
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        # 👇 Save the post to the Posts table
        db_cursor.execute(
            """
            INSERT INTO Posts (
                user_id,
                category_id,
                title,
                content,
                image_url,
                publication_date,
                approved
            )
            VALUES (?, ?, ?, ?, ?, ?, false)
        """,
            (
                post["user_id"],  # 👈 Who made the post
                post["category_id"],  # 👈 What category it’s in
                post["title"],  # 👈 Title from the form
                post["content"],  # 👈 Main body text
                post.get("image_url", ""),  # 👈 Optional image URL
                datetime.now(),  # 👈 Set to right now
            ),
        )

        # ✅ Get the ID of the new post
        new_post_id = db_cursor.lastrowid

        # 🎁 Give back the ID to the frontend
        return {"id": new_post_id}


def get_all_posts(post):
    """
    Checks for the posts in the database

    Args:
        user (dict): Contains what all is defined in one single posts and appends multiple posts into the empty "posts" list

    Returns:
        dict: {
            "valid": True,
            "token": "rare_token_user_<id>"
        }
        or {
            "valid": False
        }
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
                """
                SELECT 
                p.id,
                p.user_id, 
                p.title,
                p.category_id, 
                u.first_name,
                u.last_name,
                c.label
                FROM Posts p
                JOIN User u ON u.id = p.user_id
                JOIN Category ON c.id = p.category_id
                """,
                (post["id"]
            ))

        query_results = db_cursor.fetchall()
        posts = []
        for row in query_results:
            user = {
                "id": row["user_id"],
                "first_name": row["user_first_name"],
                "last_name": row["user_last_name"],
            }

            category = {
                "id": row["category_id"],
                "label": row["category_label"],
            }

            post = {
                "id": row["id"],
                "user_id": row["user_id"],
                "user": user,
                "category_id": row["category_id"],
                "category": category,
                "created_at": row["created_at"] if row["created_at"] is not None else ""
            }
        posts.append(post)

        # else:
        #     # Fallback: just return the basic order info
        #     db_cursor.execute(
        #         """
        #         SELECT
        #             id,
        #             metal_id,
        #             size_id,
        #             style_id
        #         FROM "Order"
        #         """
        #     )
        #     query_results = db_cursor.fetchall()
        #     orders = [dict(row) for row in query_results]

        serialized_posts = json.dumps(posts)

    return serialized_posts