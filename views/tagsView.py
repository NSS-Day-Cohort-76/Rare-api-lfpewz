from models.tags import create_tag
from models.tags import get_tags
from models.tags import delete_tag
from models.tags import update_tag


def handle_create_tag(body):
    """
    Handles creating a new tag.

    Args:
        body (dict): The JSON data from the request.

    Returns:
        tuple: (status_code, response_body)
    """
    if "label" not in body or not body["label"]:
        return (400, {"error": "Tag label is required"})
    result = create_tag(body)
    if "error" in result:
        return (400, result)
    return (201, result)


def handle_get_tags():
    tags = get_tags()
    return (200, tags)


def handle_delete_tag(tag_id):
    success = delete_tag(tag_id)
    if success:
        return (204, {})  # 204 No Content
    else:
        return (404, {"error": "Tag not found"})


def handle_update_tag(tag_id, data):
    if "label" not in data or not data["label"]:
        return (400, {"error": "Tag label is required"})
    success = update_tag(tag_id, data["label"])
    if success:
        return (204, {})  # 204 No Content
    else:
        return (404, {"error": "Tag not found"})
