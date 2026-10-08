import streamlit as st
import database

# 모듈 로드 예외 처리 (팀원들이 아직 파일을 안 만들었을 때를 대비)
try:
    from views import home, registration, search, chat, mypage
except ImportError:
    st.error("views 폴더와 내부 파이썬 파일들을 확인해주세요.")

# ======== 세션 상태 초기화 ========
if "login" not in st.session_state:
    st.session_state.login = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "page" not in st.session_state:
    st.session_state.page = "home"

# ======== 사이드바 레이아웃 ========
def render_sidebar():
    st.sidebar.title("PKNU FINDER")
    menu = st.sidebar.radio("메뉴 이동", ["홈", "분실물 등록", "채팅", "마이페이지"])
    return menu

# ======== [담당 파트] 상단 로그인/로그아웃 버튼 ========
def render_auth_buttons():
    cols = st.columns([8, 2])
    with cols[1]:
        if st.session_state.login:
            if st.button("로그아웃", key="logout_btn"):
                st.session_state.login = False
                st.session_state.user_id = None
                st.session_state.page = "home"
                st.rerun()
        else:
            if st.button("회원가입/로그인", key="login_btn"):
                st.session_state.page = "login"
                st.rerun()

# ======== 메인 라우팅 ========
def main():
    menu = render_sidebar()
    render_auth_buttons()

    # 로그인 상태에서 로그인 페이지 접근 제어
    if st.session_state.login and st.session_state.page == "login":
        st.session_state.page = "home"
        st.rerun()

    # 페이지 라우팅
    if st.session_state.page == "login":
        if 'mypage' in globals(): mypage.login_page()
        return

    if menu == "홈":
        if 'home' in globals(): home.home_page()
    elif menu == "분실물 등록":
        if 'registration' in globals(): registration.lost_registration_page()
    elif menu == "분실물 검색":
        if 'registration' in globals(): search.search_page()
    elif menu == "채팅":
        if 'chat' in globals(): chat.chat_page()
    elif menu == "마이페이지":
        if 'mypage' in globals(): mypage.mypage_screen()

if __name__ == "__main__":
    st.set_page_config(page_title="PKNU FINDER", page_icon="🎒", layout="centered")
    main()
