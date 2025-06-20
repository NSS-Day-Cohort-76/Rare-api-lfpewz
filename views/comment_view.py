from urllib.parse import parse_qs
import json
from models.comment import (
    create_comment,
    get_comments_by_post,
    update_comment,
    delete_comment,
    get_comment_by_id,
)


def handle_get_comments(resource, query_params):
    post_id = query_params.get("post_id", [None])[0]
    if post_id is not None:
        comments = get_comments_by_post(int(post_id))
        return (200, comments)
    else:
        return (400, {"message": "Missing post_id query parameter"})


def handle_create_comment(body):
    try:
        new_comment = create_comment(body)
        return (201, new_comment)
    except KeyError as e:
        return (400, {"message": f"Missing required field: {str(e)}"})


def handle_update_comment(id, body):
    update_comment(id, body)
    return (204, None)


def handle_delete_comment(id):
    delete_comment(id)
    return (204, None)


def handle_get_comment_by_id(comment_id):
    comment = get_comment_by_id(comment_id)
    if comment:
        return 200, comment
    else:
        return 404, {"error": "Comment not found"}
