import sqlite3
from datetime import datetime


def create_comment(comment):
    created_on = datetime.now().isoformat()

    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
            INSERT INTO Comments (
                post_id,
                author_id,
                subject,
                content,
                created_on
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                comment["post_id"],
                comment["author_id"],
                comment["subject"],
                comment["content"],
                created_on,
            ),
        )

        new_comment_id = db_cursor.lastrowid

    return {
        "id": new_comment_id,
        "post_id": comment["post_id"],
        "author_id": comment["author_id"],
        "subject": comment["subject"],
        "content": comment["content"],
        "created_on": created_on,
    }


def get_comments_by_post(post_id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT 
                c.id,
                c.post_id,
                c.author_id,
                c.subject,
                c.content,
                c.created_on,
                u.username
            FROM Comments c
            JOIN Users u ON c.author_id = u.id
            WHERE c.post_id = ?
            ORDER BY c.created_on ASC
            """,
            (post_id,),
        )

        return [dict(row) for row in db_cursor.fetchall()]


def get_comment_by_id(comment_id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT 
                c.id,
                c.post_id,
                c.author_id,
                c.subject,
                c.content,
                c.created_on,
                u.username
            FROM Comments c
            JOIN Users u ON c.author_id = u.id
            WHERE c.id = ?
            """,
            (comment_id,),
        )

        data = db_cursor.fetchone()

        if data:
            return {
                "id": data["id"],
                "post_id": data["post_id"],
                "author_id": data["author_id"],
                "subject": data["subject"],
                "content": data["content"],
                "created_on": data["created_on"],
                "username": data["username"],
            }


def update_comment(comment_id, updated_comment):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
            UPDATE Comments
            SET subject = ?, content = ?
            WHERE id = ?
            """,
            (updated_comment["subject"], updated_comment["content"], comment_id),
        )


def delete_comment(comment_id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
            DELETE FROM Comments
            WHERE id = ?
            """,
            (comment_id,),
        )
