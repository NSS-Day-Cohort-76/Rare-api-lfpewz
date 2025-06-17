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
            VALUES (?, ?, ?, ?, ?, ?, 1)
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
