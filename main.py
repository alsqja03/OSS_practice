import database
import streamlit as st

# 1. 페이지 설정은 최상단에서 단 1회만 호출해야 합니다.
st.set_page_config(
    page_title="PKNU FINDER",
    page_icon="🎒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. 데이터베이스 초기화 (테이블 자동 생성)
database.init_db()


# 3. 세션 상태(Session State) 초기화
def init_session():
    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = False
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "username" not in st.session_state:
        st.session_state.username = None


def main():
    init_session()

    # 사이드바 상단 브랜드 표시
    st.sidebar.title("🎒 PKNU FINDER")

    # 로그인 상태 메시지 및 로그아웃 버튼
    if st.session_state.is_logged_in:
        st.sidebar.success(f"**{st.session_state.username}**님 환영합니다!")
        if st.sidebar.button("로그아웃", use_container_width=True):
            st.session_state.is_logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.rerun()
        st.sidebar.markdown("---")

    # 사이드바 내비게이션 메뉴
    menu_options = ["홈", "분실물 검색", "습득물 등록", "채팅", "마이페이지"]
    menu = st.sidebar.radio("메뉴 선택", menu_options)

    # dynamically import views (동적 모듈 로드)
    try:
        from views import chat, home, mypage, registration, search
    except ImportError as e:
        st.error(f"뷰 모듈을 불러오는 중 오류가 발생했습니다: {e}")
        return

    # 메뉴별 페이지 라우팅
    if menu == "홈":
        if hasattr(home, "home_screen"):
            home.home_screen()
        elif hasattr(home, "home_page"):
            home.home_page()
        else:
            st.info("홈 페이지 화면입니다.")

    elif menu == "분실물 검색":
        if hasattr(search, "search_screen"):
            search.search_screen()
        elif hasattr(search, "search_page"):
            search.search_page()
        else:
            st.info("분실물 검색 페이지 화면입니다.")

    elif menu == "습득물 등록":
        if hasattr(registration, "registration_screen"):
            registration.registration_screen()
        elif hasattr(registration, "registration_page"):
            registration.registration_page()
        else:
            st.info("습득물 등록 페이지 화면입니다.")

    elif menu == "채팅":
        if hasattr(chat, "chat_screen"):
            chat.chat_screen()
        elif hasattr(chat, "chat_page"):
            chat.chat_page()
        else:
            st.info("채팅 페이지 화면입니다.")

    elif menu == "마이페이지":
        if hasattr(mypage, "mypage_screen"):
            mypage.mypage_screen()
        elif hasattr(mypage, "mypage_page"):
            mypage.mypage_page()
        else:
            st.info("마이페이지 화면입니다.")


if __name__ == "__main__":
    main()
