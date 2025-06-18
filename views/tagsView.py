from models.tags import create_tag


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
