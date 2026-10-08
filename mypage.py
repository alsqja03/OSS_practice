import streamlit as st
import database

# ======== [담당 파트] 로그인 / 회원가입 페이지 ========
def login_page():
    st.title("회원가입 / 로그인")
    tab1, tab2 = st.tabs(["🔑 로그인", "📝 회원가입"])

    with tab1:
        st.subheader("로그인")
        username = st.text_input("아이디", key="login_id")
        password = st.text_input("비밀번호", type="password", key="login_pw")
        if st.button("로그인", key="do_login"):
            user_id = database.check_login(username, password)
            if user_id:
                st.session_state.login = True
                st.session_state.user_id = user_id
                st.session_state.page = "home"
                st.success("로그인 성공!")
                st.rerun()
            else:
                st.error("아이디 또는 비밀번호가 일치하지 않습니다.")

    with tab2:
        st.subheader("회원가입")
        reg_id = st.text_input("아이디", key="reg_id")
        reg_pw = st.text_input("비밀번호", type="password", key="reg_pw")
        if st.button("회원가입", key="do_reg"):
            if not reg_id or not reg_pw:
                st.warning("아이디와 비밀번호를 모두 입력하세요.")
            else:
                if database.create_user(reg_id, reg_pw):
                    st.success("회원가입 성공! 로그인 탭에서 로그인 해주세요.")
                else:
                    st.error("이미 존재하는 아이디입니다.")

# ======== [담당 파트] 마이페이지 (북마크, 내 글, 탈퇴) ========
def mypage_screen():
    if not st.session_state.login:
        st.info("마이페이지 사용을 위해 로그인하세요.")
        if st.button("로그인 페이지로 이동"):
            st.session_state.page = "login"
            st.rerun()
        return

    # 환영 문구
    username = database.get_username(st.session_state.user_id)
    st.title("👤 마이페이지")
    st.write(f"환영합니다, **{username}**님!")
    st.markdown("---")

    # 탭으로 북마크와 내 글 분리
    tab1, tab2 = st.tabs(["📌 북마크한 분실물", "📝 내가 작성한 글"])
    
    with tab1:
        bookmarks = database.get_bookmarked_items(st.session_state.user_id)
        if bookmarks:
            for item in bookmarks:
                cols = st.columns([8, 2])
                cols[0].write(f"**{item[1]}**  |  {item[2]}  |  {item[3]}")
                # 북마크 취소 버튼
                if cols[1].button("취소", key=f"rm_bm_{item[0]}"):
                    database.remove_bookmark(st.session_state.user_id, item[0])
                    st.rerun()
        else:
            st.info("북마크한 항목이 없습니다.")

    with tab2:
        my_items = database.get_my_items(st.session_state.user_id)
        if my_items:
            for item in my_items:
                st.write(f"**{item[1]}**  |  {item[2]}  |  {item[3]}")
        else:
            st.info("작성한 글이 없습니다.")

    st.markdown("---")
    
    # 회원 탈퇴 기능 (위험 구역)
    with st.expander("⚠️ 계정 관리 (회원 탈퇴)"):
        st.warning("탈퇴 시 작성한 글, 채팅, 북마크 등 모든 데이터가 삭제되며 복구할 수 없습니다.")
        if st.button("회원 탈퇴", type="primary"):
            database.delete_user(st.session_state.user_id)
            st.session_state.login = False
            st.session_state.user_id = None
            st.session_state.page = "home"
            st.success("회원 탈퇴가 완료되었습니다. 이용해 주셔서 감사합니다.")
            st.rerun()
