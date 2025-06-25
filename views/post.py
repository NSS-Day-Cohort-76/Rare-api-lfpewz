from models.post import (
    create_post,
    get_all_posts,
    delete_post,
    get_most_recent_post,
    get_posts_by_category,
    get_single_post,
)
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


def handle_get_all_posts(user_id):
    posts = get_all_posts(user_id)
    return (200, posts)


# // USE THIS HANDLER TO GRAB A SINGLE POST BY ID WITH JOINED USER AND CATEGORY DATA FOR DISPLAY
# def handle_get_single_post(post_id):
#     post = get_single_post(post_id)
#     return (200, post)


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
            JOIN Categories c ON p.category_id = c.id
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
                updated_data.get("title", ""),
                updated_data.get("content", ""),
                updated_data.get("category_id", 1),  # fallback to category 1 if missing
                updated_data.get("image_url", ""),
                post_id,
            ),
        )

    return True


def handle_delete_post(post_id):
    delete_post(post_id)
    return (204, "")


def handle_get_most_recent_post():
    post = get_most_recent_post()
    if post:
        return 200, post
    else:
        return 404, {"error": "No posts found"}


def handle_get_posts_by_category(category_id):
    posts = get_posts_by_category(category_id)
    return (200, posts)


def handle_approve_post(post_id, data):
    from models.post import approve_post

    approved_value = data.get("approved")
    if approved_value is None:
        return 400, {"error": "Missing approved value"}

    approve_post(post_id, approved_value)
    return 204, {}
