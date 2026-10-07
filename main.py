import streamlit as st
import sqlite3
from datetime import datetime
import hashlib

# ======== DB 초기화 및 연결 ========
def init_db():
    conn = sqlite3.connect("pkunfinder.db", check_same_thread=False)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )""")
    c.execute("""
    CREATE TABLE IF NOT EXISTS lost_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT,
        lost_date TEXT,
        user_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )""")
    c.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        timestamp TEXT,
        FOREIGN KEY(item_id) REFERENCES lost_items(id),
        FOREIGN KEY(user_id) REFERENCES users(id)
    )""")
    conn.commit()
    return conn

conn = init_db()
cursor = conn.cursor()

# ======== 유저 로그인 상태 관리 ========
if "login" not in st.session_state:
    st.session_state.login = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "keyword" not in st.session_state:
    st.session_state.keyword = ""
if "page" not in st.session_state:
    st.session_state.page = "home"
if "selected_item" not in st.session_state:
    st.session_state.selected_item = None

# ======== 비밀번호 해싱 함수 (sha256) ========
def hash_password(password: str):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# ======== 유저 로그인 체크 ========
def check_login(username, password):
    hashed_pw = hash_password(password)
    cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (username, hashed_pw))
    user = cursor.fetchone()
    if user:
        return user[0]
    return None

# ======== 회원가입 함수 ========
def create_user(username, password):
    hashed_pw = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

# ======== 분실물 저장 ========
def save_lost_item(name, location, lost_date, user_id):
    cursor.execute("INSERT INTO lost_items (name, location, lost_date, user_id) VALUES (?, ?, ?, ?)",
                   (name, location, lost_date, user_id))
    conn.commit()

# ======== 검색 기능 ========
def search_lost_items(keyword):
    keyword_like = f"%{keyword}%"
    cursor.execute("SELECT id, name, location, lost_date FROM lost_items WHERE name LIKE ? ORDER BY lost_date DESC", (keyword_like,))
    return cursor.fetchall()

# ======== 최근 등록 분실물 조회 ========
def get_recent_lost_items(limit=3):
    cursor.execute("SELECT id, name, location, lost_date FROM lost_items ORDER BY lost_date DESC LIMIT ?", (limit,))
    return cursor.fetchall()

# ======== 채팅 저장 ========
def save_chat(item_id, user_id, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO chats (item_id, user_id, message, timestamp) VALUES (?, ?, ?, ?)", (item_id, user_id, message, timestamp))
    conn.commit()

# ======== 채팅 불러오기 ========
def get_chats(item_id):
    cursor.execute("""
        SELECT users.username, chats.message, chats.timestamp
        FROM chats JOIN users ON chats.user_id = users.id
        WHERE item_id=?
        ORDER BY timestamp ASC
        """, (item_id,))
    return cursor.fetchall()

# ======== 사이드바 메뉴 생성 ========
def sidebar_menu():
    st.sidebar.title("PKNU FINDER")
    menu = st.sidebar.radio("", ["홈", "분실물 등록", "채팅", "마이페이지"])
    st.sidebar.markdown(
        "<div style='position:absolute; bottom:10px; width:85%;'>"
        "<img src='https://upload.wikimedia.org/wikipedia/commons/8/8f/Pukyong_National_University_Logo.svg' alt='부경대학교 로고' style='width:100%; max-width:150px;'/>"
        "</div>", unsafe_allow_html=True)
    return menu

# ======== 상단 로그인/로그아웃 버튼 ========
def login_buttons():
    cols = st.columns([9,1])
    with cols[1]:
        if st.session_state.login:
            if st.button("로그아웃"):
                st.session_state.login = False
                st.session_state.user_id = None
                st.experimental_rerun()
        else:
            if st.button("회원가입/로그인"):
                login_page()
                st.stop()

# ======== 로그인 및 회원가입 페이지 ========
def login_page():
    st.title("회원가입 / 로그인")
    tab = st.radio("선택하세요:", ["로그인", "회원가입"])
    username = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")

    if tab == "회원가입":
        if st.button("회원가입"):
            if not username or not password:
                st.warning("아이디와 비밀번호를 모두 입력하세요.")
            else:
                if create_user(username, password):
                    st.success("회원가입 성공! 로그인 해주세요.")
                else:
                    st.error("이미 존재하는 아이디입니다.")
    else:
        if st.button("로그인"):
            user_id = check_login(username, password)
            if user_id:
                st.session_state.login = True
                st.session_state.user_id = user_id
                st.success(f"{username}님, 환영합니다!")
                st.experimental_rerun()
            else:
                st.error("아이디 또는 비밀번호가 일치하지 않습니다.")

# ======== 홈 화면 ========
def home_page():
    st.title("PKNU FINDER에 오신 것을 환영합니다!")
    st.write("분실물을 검색하고, 주인을 찾아주세요.")

    keyword = st.text_input("물건 이름, 장소, 키워드를 입력하세요.", st.session_state.keyword)
    if st.button("검색"):
        st.session_state.keyword = keyword
        st.experimental_rerun()

    recent_items = get_recent_lost_items()
    st.subheader("최근 등록된 분실물")
    cols = st.columns(len(recent_items))
    for idx, item in enumerate(recent_items):
        with cols[idx]:
            st.image("https://via.placeholder.com/150", width=120)
            st.write(f"**{item[1]}**")
            st.write(item[2])
            st.write(item[3])
            if st.button(f"상세보기-{item[0]}"):
                st.session_state.selected_item = item[0]
                st.experimental_rerun()

    if st.button("전체보기"):
        st.session_state.keyword = ""
        st.session_state.page = "lost_items"
        st.experimental_rerun()

# ======== 검색 결과 페이지 ========
def search_page():
    keyword = st.session_state.keyword
    st.title(f'"{keyword}" 검색 결과')
    results = search_lost_items(keyword)
    if not results:
        st.info("검색 결과가 없습니다.")
        return
    for item in results:
        st.write(f"**{item[1]}**  -  {item[2]}  -  {item[3]}")
        if st.button(f"상세보기-{item[0]}"):
            st.session_state.selected_item = item[0]
            st.experimental_rerun()

# ======== 분실물 전체보기 페이지 ========
def lost_items_page():
    st.title("전체 분실물 목록")
    cursor.execute("SELECT id, name, location, lost_date FROM lost_items ORDER BY lost_date DESC")
    items = cursor.fetchall()
    for item in items:
        st.write(f"**{item[1]}**  -  {item[2]}  -  {item[3]}")
        if st.button(f"상세보기-{item[0]}"):
            st.session_state.selected_item = item[0]
            st.experimental_rerun()

# ======== 분실물 상세 페이지 ========
def lost_detail_page():
    item_id = st.session_state.selected_item
    if not item_id:
        st.warning("잘못된 접근입니다.")
        return
    cursor.execute("SELECT name, location, lost_date FROM lost_items WHERE id=?", (item_id,))
    item = cursor.fetchone()
    if not item:
        st.warning("분실물 정보를 찾을 수 없습니다.")
        return
    st.title(item[0])
    st.write(f"분실 위치: {item[1]}")
    st.write(f"등록일: {item[2]}")
    st.image("https://via.placeholder.com/300")

    if st.session_state.login:
        if st.button("채팅하기"):
            st.session_state.page = "chat"
            st.experimental_rerun()
    else:
        st.info("채팅 기능 사용하려면 로그인하세요.")
        if st.button("로그인"):
            login_page()
            st.stop()

# ======== 분실물 등록 페이지 ========
def lost_registration_page():
    st.title("분실물 등록")
    if not st.session_state.login:
        st.info("분실물 등록을 위해 로그인하세요.")
        if st.button("로그인"):
            login_page()
            st.stop()
        return

    name = st.text_input("물건 이름")
    location = st.text_input("분실 위치")
    lost_date = st.date_input("분실 날짜")

    if st.button("등록"):
        if not name or not location:
            st.warning("모든 항목을 입력하세요.")
            return
        save_lost_item(name, location, lost_date.strftime("%Y-%m-%d"), st.session_state.user_id)
        st.success("분실물이 등록되었습니다!")
        st.experimental_rerun()

# ======== 채팅 페이지 ========
def chat_page():
    if not st.session_state.login:
        st.info("채팅 사용을 위해 로그인하세요.")
        if st.button("로그인"):
            login_page()
            st.stop()
        return

    item_id = st.session_state.selected_item
    if not item_id:
        st.info("채팅할 분실물을 선택하세요.")
        return

    st.title("채팅")
    chats = get_chats(item_id)
    for username, message, timestamp in chats:
        st.markdown(f"**{username}**  ({timestamp}): {message}")

    msg = st.text_input("메시지 입력")
    if st.button("전송") and msg.strip():
        save_chat(item_id, st.session_state.user_id, msg.strip())
        st.experimental_rerun()

# ======== 마이페이지 ========
def mypage():
    if not st.session_state.login:
        st.info("마이페이지 사용을 위해 로그인하세요.")
        if st.button("로그인"):
            login_page()
            st.stop()
        return

    st.title("마이페이지")
    cursor.execute("SELECT username FROM users WHERE id=?", (st.session_state.user_id,))
    user = cursor.fetchone()
    st.write(f"환영합니다, {user[0]}님!")

# ======== 메인 ========
def main():
    menu = sidebar_menu()
    login_buttons()

    if menu == "홈":
        if st.session_state.keyword != "":
            search_page()
        else:
            home_page()
    elif menu == "분실물 등록":
        lost_registration_page()
    elif menu == "채팅":
        chat_page()
    elif menu == "마이페이지":
        mypage()

    # 상세페이지가 선택된 상태면 항상 띄움
    if st.session_state.selected_item is not None:
        lost_detail_page()

if __name__ == "__main__":
    main()
