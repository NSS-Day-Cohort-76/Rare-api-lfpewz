from models.post_reaction import get_post_reaction, add_post_reaction, update_post_reaction

def handle_get_post_reaction(user_id, post_id):
    if not user_id or not post_id:
        return 400, {"error": "user_id and post_id are required"}
    post_reaction = get_post_reaction(user_id, post_id)
    result = [post_reaction] if post_reaction else []
    return 200, result

def handle_add_post_reaction(data):
    return add_post_reaction(data)

def handle_update_post_reaction(post_reaction_id, data):
    if "reaction_id" not in data or not data["reaction_id"]:
        return 400, {"error": "reaction_id is required"}

    reaction_id = data["reaction_id"]
    success = update_post_reaction(reaction_id, post_reaction_id)

    if success:
        return 204, {}  # No Content
    else:
        return 404, {"error": "PostReaction not found"}

