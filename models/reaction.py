import sqlite3

def get_all_reactions():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("SELECT id, label, image_url FROM Reactions")
        reactions = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            reactions.append({"id": row["id"],
                              "label": row["label"],
                              "image_url": row["image_url"]})
        return reactions