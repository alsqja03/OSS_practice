import streamlit as st
from database import get_connection, hash_password


def create_user(username, password):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hash_password(password)),
            )
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False


def check_login(username, password):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM users WHERE username = ? AND password = ?",
            (username, hash_password(password)),
        )
        result = cursor.fetchone()
        return result[0] if result else None


def delete_user(user_id):
    """
    회원 탈퇴: PRAGMA foreign_keys = ON 설정으로 users 삭제 시
    연관 데이터(lost_items, chats, bookmarks)가 CASCADE로 자동 삭제됩니다.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
        conn.commit()
