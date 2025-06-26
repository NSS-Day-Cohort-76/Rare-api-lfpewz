import sqlite3

def get_post_reaction(user_id, post_id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
            SELECT * FROM PostReactions
            WHERE user_id = ? AND post_id = ?
            """,
            (user_id, post_id),
        )
        row = db_cursor.fetchone()

        if row:
            return dict(row)
        else:
            return None


def add_post_reaction(data):
    required = ["user_id", "post_id", "reaction_id"]
    if not all(k in data and data[k] for k in required):
        return 400, {"error": "user_id, post_id, and reaction_id are required"}

    try:
        with sqlite3.connect("./db.sqlite3") as conn:
            db_cursor = conn.cursor()
            db_cursor.execute(
                """
                INSERT INTO PostReactions (user_id, post_id, reaction_id)
                VALUES (?, ?, ?)
                """,
                (data["user_id"], data["post_id"], data["reaction_id"]),
            )
            new_id = db_cursor.lastrowid

        return 201, {"message": "PostReaction created", "id": new_id}

    except Exception as e:
        return 500, {"error": f"Database error: {str(e)}"}



def update_post_reaction(reaction_id, post_reaction_id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
            UPDATE PostReactions
            SET reaction_id = ?
            WHERE id = ?
            """,
            (reaction_id, post_reaction_id),
        )
        return db_cursor.rowcount > 0
