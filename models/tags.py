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


def get_tags():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("SELECT id, label FROM Tags")
        tags = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            tags.append({"id": row["id"], "label": row["label"]})
        return tags


def delete_tag(tag_id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("DELETE FROM Tags WHERE id = ?", (tag_id,))
        return db_cursor.rowcount > 0  # True if a row was deleted


def update_tag(tag_id, label):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("UPDATE Tags SET label = ? WHERE id = ?", (label, tag_id))
        return db_cursor.rowcount > 0  # True if a row was updated
