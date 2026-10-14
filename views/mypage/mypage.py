# views/mypage.py
import database
import streamlit as st


def mypage_screen():
    st.title("👤 마이페이지")

    # ----------------------------------------------------
    # 1. 비로그인 상태일 때: 로그인 및 회원가입 화면 표시
    # ----------------------------------------------------
    if not st.session_state.get("is_logged_in") or not st.session_state.get(
        "user_id"
    ):
        st.info("로그인이 필요한 서비스입니다. 아래에서 로그인하거나 회원가입해 주세요.")

        tab_login, tab_register = st.tabs(["🔑 로그인", "📝 회원가입"])

        # --- 로그인 탭 ---
        with tab_login:
            st.subheader("로그인")
            login_id = st.text_input("아이디", key="mypage_login_id")
            login_pw = st.text_input(
                "비밀번호", type="password", key="mypage_login_pw"
            )

            if st.button(
                "로그인", key="mypage_login_btn", use_container_width=True
            ):
                if not login_id.strip() or not login_pw.strip():
                    st.warning("아이디와 비밀번호를 모두 입력해 주세요.")
                else:
                    user_id = database.check_login(login_id, login_pw)
                    if user_id:
                        st.session_state.is_logged_in = True
                        st.session_state.user_id = user_id
                        st.session_state.username = login_id
                        st.success(f"{login_id}님, 환영합니다!")
                        st.rerun()
                    else:
                        st.error("아이디 또는 비밀번호가 올바르지 않습니다.")

        # --- 회원가입 탭 ---
        with tab_register:
            st.subheader("회원가입")
            reg_id = st.text_input("새 아이디", key="mypage_reg_id")
            reg_pw = st.text_input(
                "새 비밀번호", type="password", key="mypage_reg_pw"
            )
            reg_pw_confirm = st.text_input(
                "비밀번호 확인", type="password", key="mypage_reg_pw_confirm"
            )

            if st.button(
                "회원가입", key="mypage_reg_btn", use_container_width=True
            ):
                if not reg_id.strip() or not reg_pw.strip():
                    st.warning("아이디와 비밀번호를 모두 입력해 주세요.")
                elif reg_pw != reg_pw_confirm:
                    st.error("비밀번호 확인이 일치하지 않습니다.")
                else:
                    success = database.create_user(reg_id, reg_pw)
                    if success:
                        st.success(
                            "회원가입이 완료되었습니다! 로그인 탭에서 로그인해 주세요."
                        )
                    else:
                        st.error("이미 존재하는 아이디입니다.")

        return  # 비로그인 처리 완료 후 종료

    # ----------------------------------------------------
    # 2. 로그인된 상태일 때: 마이페이지 정보 표시
    # ----------------------------------------------------
    user_id = st.session_state.user_id
    username = database.get_username(user_id)

    if not username:
        st.error("사용자 정보를 불러올 수 없습니다.")
        return

    st.success(f"**{username}**님, 환영합니다! 🎉")
    st.markdown("---")

    # 탭 구성 (내 작성글 / 북마크 목록 / 계정 관리)
    tab1, tab2, tab3 = st.tabs(
        ["📦 내가 등록한 물품", "⭐ 북마크 목록", "⚙️ 계정 관리"]
    )

    # --- 탭 1: 내가 등록한 물품 목록 ---
    with tab1:
        st.subheader("내가 등록한 물품 목록")
        my_items = database.get_my_items(user_id)

        if my_items:
            for item in my_items:
                item_id, name, location, lost_date = item
                with st.expander(f"📍 {name} (습득 장소: {location or '미지정'})"):
                    st.write(f"**분실/습득일:** {lost_date or '정보 없음'}")
                    st.write(f"**물품 ID:** {item_id}")
        else:
            st.info("등록한 물품이 없습니다.")

    # --- 탭 2: 북마크 목록 ---
    with tab2:
        st.subheader("북마크한 물품 목록")
        bookmarked_items = database.get_bookmarked_items(user_id)

        if bookmarked_items:
            for item in bookmarked_items:
                item_id, name, location, lost_date = item
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(
                        f"**{name}** | 장소: {location or '미지정'} | 날짜: {lost_date or '정보 없음'}"
                    )
                with col2:
                    if st.button("북마크 해제", key=f"unbookmark_{item_id}"):
                        database.remove_bookmark(user_id, item_id)
                        st.toast("북마크가 해제되었습니다.")
                        st.rerun()
        else:
            st.info("북마크한 물품이 없습니다.")

    # --- 탭 3: 계정 관리 및 회원 탈퇴 ---
    with tab3:
        st.subheader("계정 관리")
        st.write(f"**아이디:** {username}")

        st.markdown("---")
        st.caption(
            "🚨 계정을 삭제하면 작성한 게시글, 채팅, 북마크 내역이 모두 삭제됩니다."
        )

        confirm_withdraw = st.checkbox("정말로 회원 탈퇴하시겠습니까?")
        if st.button(
            "회원 탈퇴 실행", type="primary", disabled=not confirm_withdraw
        ):
            database.delete_user(user_id)
            st.session_state.is_logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.success("회원 탈퇴가 완료되었습니다.")
            st.rerun()


# main.py 호환용 에일리어스
mypage_page = mypage_screen
