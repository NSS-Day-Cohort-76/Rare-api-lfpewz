from models.post import create_post


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
