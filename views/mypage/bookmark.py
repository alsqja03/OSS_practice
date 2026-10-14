from database import get_connection


def add_bookmark(user_id, item_id):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO bookmarks (user_id, item_id) VALUES (?, ?)",
                (user_id, item_id),
            )
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False  # 이미 북마크한 경우


def remove_bookmark(user_id, item_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM bookmarks WHERE user_id=? AND item_id=?",
            (user_id, item_id),
        )
        conn.commit()


def get_bookmarked_items(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT l.id, l.name, l.location, l.lost_date 
            FROM lost_items l
            JOIN bookmarks b ON l.id = b.item_id
            WHERE b.user_id = ?
            ORDER BY l.lost_date DESC
        """,
            (user_id,),
        )
        return cursor.fetchall()


def get_my_items(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, location, lost_date FROM lost_items WHERE user_id=? ORDER BY lost_date DESC",
            (user_id,),
        )
        return cursor.fetchall()
