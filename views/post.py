from models.post import create_post, get_all_posts
import sqlite3


def handle_create_post(body):
    """
    Handles creating a new post.

    Args:
        body (dict): The JSON data from the request.

    Returns:
        tuple: (status_code, response_body)
    """
    # 🔁 Ask the model to save the post in the database
    result = create_post(body)

    # ✅ Send back the new post's ID with status 201 (Created)
    return (201, result)


def handle_get_all_posts():
    posts = get_all_posts()
    return (200, posts)

def handle_get_post(post_id):
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
                u.username
            FROM Posts p
            JOIN Users u ON p.user_id = u.id
            WHERE p.id = ?
        """,
            (post_id,),
        )

        row = db_cursor.fetchone()

        if row:
            return {
                "id": row["id"],
                "title": row["title"],
                "content": row["content"],
                "image_url": row["image_url"],
                "publication_date": row["publication_date"],
                "user_id": row["user_id"],
                "author": row["username"],
            }
        else:
            return None


def handle_update_post(post_id, updated_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            UPDATE Posts
            SET title = ?, content = ?, category_id = ?, image_url = ?
            WHERE id = ?
        """,
            (
                updated_data["title"],
                updated_data["content"],
                updated_data["category_id"],
                updated_data.get("image_url", ""),
                post_id,
            ),
        )

    return True
