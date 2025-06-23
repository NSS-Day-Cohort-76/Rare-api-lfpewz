import sqlite3
from datetime import datetime


def login_user(user):
    """
    Checks for the user in the database

    Args:
        user (dict): Contains the username and password of the user trying to login

    Returns:
        dict: {
            "valid": True,
            "token": "rare_token_user_<id>"
        }
        or {
            "valid": False
        }
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT id, username
            FROM Users
            WHERE username = ? AND password = ?
            """,
            (user["username"], user["password"]),
        )

        user_from_db = db_cursor.fetchone()

        if user_from_db is not None:
            user_id = user_from_db["id"]
            # isStaff = user_from_db["isStaff"]  # Adjust this key as needed
            return {"valid": True, "user_id": user_id}
        else:
            return {"valid": False}

        # if user_from_db is not None:
        #     user_id = user_from_db["id"]
        #     return {"valid": True, "token": user_id}
        #     # return {"valid": True, "token": f"rare_token_user_{user_id}"}
        # else:
        #     return {"valid": False}


def create_user(user):
    """
    Adds a user to the database when they register

    Args:
        user (dict): The dictionary passed to the register POST request

    Returns:
        dict: {
            "id": <new_user_id>
        }
        or {
            "error": "..."
        }
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Check for duplicate email
        db_cursor.execute("SELECT id FROM Users WHERE email = ?", (user["email"],))
        if db_cursor.fetchone():
            return {"error": "Email already in use"}

        # Check for duplicate username
        db_cursor.execute(
            "SELECT id FROM Users WHERE username = ?", (user["username"],)
        )
        if db_cursor.fetchone():
            return {"error": "Username already taken"}

        db_cursor.execute(
            """
            INSERT INTO Users (
                first_name,
                last_name,
                username,
                email,
                password,
                bio,
                created_on,
                active,
                isStaff
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, 1, 1)
            """,
            (
                user["first_name"],
                user["last_name"],
                user["username"],
                user["email"],
                user["password"],
                user["bio"],
                datetime.now()
            ),
        )

        return {"id": db_cursor.lastrowid}
