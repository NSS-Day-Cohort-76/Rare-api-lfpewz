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
    
def create_category(body):
    required_fields = ["label"]  # ✅ Corrected from "category_id" to "label"
    for field in required_fields:
        if field not in body:
            return 400, {"error": f"Missing field: {field}"}

    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
            INSERT INTO Categories (label)  -- ✅ Ensure this table name is correct
            VALUES (?)
            """,
            (body["label"],),  # ✅ Corrected tuple syntax
        )
        category_id = db_cursor.lastrowid

    return 201, {"id": category_id, "message": "Category created"}

def delete_category(category_id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("DELETE FROM Categories WHERE id = ?", (category_id,))

def update_category(label, category_id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute(
            "UPDATE Categories SET label = ? WHERE id = ?",
            (label, category_id)
        )
        return db_cursor.rowcount > 0  # True if a row was updated


