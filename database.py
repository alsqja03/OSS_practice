import sqlite3
import hashlib
from datetime import datetime

DB_NAME = "pkunfinder.db"

# ======== DB 초기화 및 연결 ========
def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cursor = conn.cursor()
    
    # 1. users 테이블
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )""")
    
    # 2. lost_items 테이블
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lost_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT,
        lost_date TEXT,
        user_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )""")
    
    # 3. chats 테이블
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        timestamp TEXT,
        FOREIGN KEY(item_id) REFERENCES lost_items(id) ON DELETE CASCADE,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )""")

    # 4. bookmarks 테이블 (북마크 기능)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookmarks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY(item_id) REFERENCES lost_items(id) ON DELETE CASCADE,
        UNIQUE(user_id, item_id)
    )""")
    
    conn.commit()
    return conn

conn = init_db()
cursor = conn.cursor()

# SQLite 외래키 제약조건(CASCADE) 활성화 (탈퇴 시 연관 데이터 자동 삭제용)
cursor.execute("PRAGMA foreign_keys = ON")

def hash_password(password: str):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

# ======== [담당 파트] 회원 관리 (가입, 로그인, 탈퇴) ========
def create_user(username, password):
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                       (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def check_login(username, password):
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", 
                   (username, hash_password(password)))
    result = cursor.fetchone()
    return result[0] if result else None

def get_username(user_id):
    cursor.execute("SELECT username FROM users WHERE id=?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else None

def delete_user(user_id):
    # 회원 탈퇴: 회원이 쓴 글, 채팅, 북마크 내역, 계정을 모두 삭제합니다.
    cursor.execute("DELETE FROM chats WHERE user_id=?", (user_id,))
    cursor.execute("DELETE FROM bookmarks WHERE user_id=?", (user_id,))
    cursor.execute("DELETE FROM lost_items WHERE user_id=?", (user_id,))
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()

# ======== [담당 파트] 마이페이지 및 북마크 로직 ========
def add_bookmark(user_id, item_id):
    try:
        cursor.execute("INSERT INTO bookmarks (user_id, item_id) VALUES (?, ?)", (user_id, item_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False # 이미 북마크한 경우

def remove_bookmark(user_id, item_id):
    cursor.execute("DELETE FROM bookmarks WHERE user_id=? AND item_id=?", (user_id, item_id))
    conn.commit()

def get_bookmarked_items(user_id):
    cursor.execute("""
        SELECT l.id, l.name, l.location, l.lost_date 
        FROM lost_items l
        JOIN bookmarks b ON l.id = b.item_id
        WHERE b.user_id = ?
        ORDER BY l.lost_date DESC
    """, (user_id,))
    return cursor.fetchall()

def get_my_items(user_id):
    cursor.execute("SELECT id, name, location, lost_date FROM lost_items WHERE user_id=? ORDER BY lost_date DESC", (user_id,))
    return cursor.fetchall()
