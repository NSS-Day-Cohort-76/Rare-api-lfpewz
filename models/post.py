import sqlite3
from datetime import datetime


def create_post(post):
    """
    Adds a new post to the Posts table.

    Args:
        post (dict): The post data from the frontend.

    Returns:
        dict: The newly created post as a dictionary
    """
    publication_date = datetime.now().isoformat()
    image_url = post.get("image_url", "")  # Optional

    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

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
                post["user_id"],
                post["category_id"],
                post["title"],
                post["content"],
                image_url,
                publication_date,
            ),
        )

        new_post_id = db_cursor.lastrowid

    # Return the full post object
    return {
        "id": new_post_id,
        "user_id": post["user_id"],
        "category_id": post["category_id"],
        "title": post["title"],
        "content": post["content"],
        "image_url": image_url,
        "publication_date": publication_date,
        "approved": True,
    }
