from models.post import (
    create_post,
    get_all_posts,
    delete_post,
    get_most_recent_post,
    get_posts_by_category,
    get_single_post,
    approve_post,
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
    post = get_single_post(post_id)
    if post:
        return 200, post
    return 404, {"error": "Post not found"}


def handle_update_post(post_id, updated_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        if "approved" in updated_data:
            db_cursor.execute(
                """
                UPDATE Posts
                SET approved = ?
                WHERE id = ?
                """,
                (updated_data["approved"], post_id),
            )
        else:
            db_cursor.execute(
                """
                UPDATE Posts
                SET title = ?, content = ?, category_id = ?, image_url = ?
                WHERE id = ?
                """,
                (
                    updated_data.get("title", ""),
                    updated_data.get("content", ""),
                    updated_data.get("category_id", 1),
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
    # data should be a dict with an "approved" key: 1 (approve), 0 (pending), -1 (deny)
    approved_value = data.get("approved")
    if approved_value not in [-1, 0, 1]:
        return 400, {"error": "Invalid approval value"}
    approve_post(post_id, approved_value)
    return 204, {}
