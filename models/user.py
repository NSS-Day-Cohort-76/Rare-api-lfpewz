import sqlite3
from datetime import datetime


def login_user(user):
    """
    Checks for the user in the database

    Args:
        user (dict): Contains the username and password of the user trying to login

    Returns:
        dict: If the user was found will return valid boolean of True and the user's id as the token
              If the user was not found will return valid boolean False
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
            return {"valid": True, "token": user_from_db["id"]}
        else:
            return {"valid": False}


def create_user(user):
    """
    Adds a user to the database when they register

    Args:
        user (dict): The dictionary passed to the register POST request

    Returns:
        dict: If successful, returns {'id': new_user_id}
              If duplicate, returns {'error': '...'}
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
                first_name, last_name, username, email,
                password, bio, created_on, active
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, 1)
            """,
            (
                user["first_name"],
                user["last_name"],
                user["username"],
                user["email"],
                user["password"],
                user["bio"],
                datetime.now(),
            ),
        )

        return {"id": db_cursor.lastrowid}
