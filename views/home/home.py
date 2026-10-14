import streamlit as st
from database import get_connection


def get_recent_items(limit=5):
    """데이터베이스에서 최근 등록된 분실물 목록을 조회합니다."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, name, location, lost_date, user_id 
            FROM lost_items 
            ORDER BY id DESC 
            LIMIT ?
            """,
            (limit,),
        )
        return cursor.fetchall()


def render_home():
    """홈 화면을 렌더링합니다."""
    
    # 1. 상단 배너 영역
    st.markdown(
        """
        <div style="padding: 30px; background-color: #f0f2f6; border-radius: 10px; text-align: center; margin-bottom: 25px;">
            <h1 style="color: #31333F; margin: 0;">📢 PKNU Finder 배너 영역</h1>
            <p style="color: #6c757d; margin-top: 10px;">교내 분실물을 손쉽게 찾고 등록하세요!</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 2. 최근 등록 게시글 영역
    st.markdown("### 📋 최근 등록 게시글")
    
    recent_items = get_recent_items(limit=5)

    if not recent_items:
        st.info("아직 등록된 분실물 게시글이 없습니다.")
    else:
        for item in recent_items:
            item_id, name, location, lost_date, user_id = item
            
            # 각 게시글을 컨테이너(카드 형태)로 시각화
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**물품명:** {name}")
                    st.write(f"📍 **장소:** {location or '장소 미입력'} | 📅 **날짜:** {lost_date or '날짜 미입력'}")
                with col2:
                    # 상세 보기 버튼 (추후 상세 페이지나 모달 기능과 연동 가능)
                    if st.button("상세 보기", key=f"home_item_{item_id}", use_container_width=True):
                        st.session_state[f"selected_item_id"] = item_id
                        st.success(f"'{name}' 선택됨")
