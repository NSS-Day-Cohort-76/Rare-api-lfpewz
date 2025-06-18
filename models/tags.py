import sqlite3


def create_tag(tag):
    """
    Inserts a new tag into the Tags table.

    Args:
        tag (dict): The tag data from the frontend.

    Returns:
        dict: Contains the ID of the new tag like { "id": 3 }
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        # Optional: Check for duplicate label
        db_cursor.execute("SELECT id FROM Tags WHERE label = ?", (tag["label"],))
        if db_cursor.fetchone():
            return {"error": "Tag label already exists"}

        db_cursor.execute(
            """
            INSERT INTO Tags (label)
            VALUES (?)
            """,
            (tag["label"],),
        )
        new_tag_id = db_cursor.lastrowid
        return {"id": new_tag_id}
