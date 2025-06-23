from models.user import get_all_users


def handle_get_all_users():
    users = get_all_users()
    sorted_users = sorted(users, key=lambda u: u["display_name"].lower())
    return 200, sorted_users
