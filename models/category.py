import sqlite3

def get_all_categories():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("SELECT id, label FROM Categories")
        categories = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            categories.append({"id": row["id"], "label": row["label"]})
        return categories