# views/mypage.py
import database
import streamlit as st


def mypage_screen():
    st.title("👤 마이페이지")

    # 1. 로그인 여부 확인
    if not st.session_state.get("is_logged_in") or not st.session_state.get(
        "user_id"
    ):
        st.warning("로그인이 필요한 페이지입니다. 먼저 로그인해 주세요.")
        return

    user_id = st.session_state.user_id

    # 2. 유저 이름 조회
    username = database.get_username(user_id)
    if not username:
        st.error("사용자 정보를 불러올 수 없습니다.")
        return

    st.success(f"**{username}**님, 환영합니다! 🎉")
    st.markdown("---")

    # 3. 탭 구성 (내 작성글 / 북마크 목록 / 계정 관리)
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
                    st.write(f"**{name}** | 장소: {location or '미지정'} | 날짜: {lost_date or '정보 없음'}")
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
        st.caption("🚨 계정을 삭제하면 작성한 게시글, 채팅, 북마크 내역이 모두 삭제됩니다.")
        
        # 회원 탈퇴 확인 체크박스 및 버튼
        confirm_withdraw = st.checkbox("정말로 회원 탈퇴하시겠습니까?")
        if st.button("회원 탈퇴 실행", type="primary", disabled=not confirm_withdraw):
            database.delete_user(user_id)
            # 세션 초기화 및 로그아웃
            st.session_state.is_logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.success("회원 탈퇴가 완료되었습니다. 이용해 주셔서 감사합니다.")
            st.rerun()


# main.py 호환을 위한 에일리어스
mypage_page = mypage_screen
