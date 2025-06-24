import sqlite3
from models.user import get_all_users


def handle_get_all_users():
    users = get_all_users()
    sorted_users = sorted(users, key=lambda u: u["display_name"].lower())
    return 200, sorted_users


import sqlite3


def handle_update_user(id, user_data):
    print("🔁 Incoming user update payload:", user_data)

    active = user_data.get("active")
    is_staff = user_data.get("is_staff")

    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            UPDATE Users
            SET active = ?, isStaff = ?
            WHERE id = ?
            """,
            (active, is_staff, id),
        )

    return {"message": "User updated"}
