import streamlit as st
from views.mypage.user import delete_user
from views.mypage.bookmark import (
    get_bookmarked_items,
    get_my_items,
    remove_bookmark,
)
from database import get_username


def render_mypage():
    st.title("👤 마이페이지")

    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("로그인이 필요합니다.")
        return

    username = get_username(user_id)
    st.subheader(f"안녕하세요, **{username}**님!")

    tab1, tab2, tab3 = st.tabs(
        ["내가 등록한 분실물", "북마크한 목록", "회원 설정"]
    )

    with tab1:
        st.markdown("### 내가 등록한 분실물")
        my_items = get_my_items(user_id)
        if not my_items:
            st.info("등록한 분실물이 없습니다.")
        else:
            for item in my_items:
                item_id, name, location, lost_date = item
                with st.container(border=True):
                    st.write(f"**물품명:** {name}")
                    st.write(f"**장소:** {location}")
                    st.write(f"**날짜:** {lost_date}")

    with tab2:
        st.markdown("### 북마크한 분실물")
        bookmarked_items = get_bookmarked_items(user_id)
        if not bookmarked_items:
            st.info("북마크한 분실물이 없습니다.")
        else:
            for item in bookmarked_items:
                item_id, name, location, lost_date = item
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"**물품명:** {name} | **장소:** {location} ({lost_date})")
                with col2:
                    if st.button("북마크 해제", key=f"unbookmark_{item_id}"):
                        remove_bookmark(user_id, item_id)
                        st.success("북마크가 해제되었습니다.")
                        st.rerun()

    with tab3:
        st.markdown("### 회원 탈퇴")
        st.warning("계정을 삭제하면 등록한 분실물과 채팅, 북마크 데이터가 모두 삭제됩니다.")
        if st.button("회원 탈퇴하기", type="primary"):
            delete_user(user_id)
            st.session_state.clear()
            st.success("회원 탈퇴가 완료되었습니다.")
            st.rerun()
