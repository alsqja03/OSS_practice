import streamlit as st
from database import get_connection


def search_items(keyword="", category="전체", start_date=None, end_date=None):
    """조건에 따른 분실물 검색 쿼리를 실행합니다."""
    with get_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT id, name, location, lost_date FROM lost_items WHERE 1=1"
        params = []

        if keyword:
            query += " AND (name LIKE ? OR location LIKE ?)"
            params.extend([f"%{keyword}%", f"%{keyword}%"])

        if category and category != "전체":
            # 예시: 카테고리가 태그나 이름에 포함된다고 가정
            query += " AND name LIKE ?"
            params.append(f"%{category}%")

        if start_date:
            query += " AND lost_date >= ?"
            params.append(str(start_date))

        if end_date:
            query += " AND lost_date <= ?"
            params.append(str(end_date))

        query += " ORDER BY lost_date DESC"
        cursor.execute(query, params)
        return cursor.fetchall()


def render_search():
    st.title("🔎 분실물 검색")

    # 1. 상단 검색바 영역
    col_search, col_btn = st.columns([4, 1])
    with col_search:
        keyword = st.text_input("검색어 입력", placeholder="물품명 또는 장소를 입력하세요", label_visibility="collapsed")
    with col_btn:
        search_clicked = st.button("검색", use_container_width=True)

    # 2. 필터 영역 (카테고리, 시작날짜, 종료날짜, 필터적용, 초기화)
    with st.container(border=True):
        f_col1, f_col2, f_col3, f_col4, f_col5 = st.columns([2, 2, 2, 1, 1])
        with f_col1:
            category = st.selectbox("카테고리", ["전체", "전자기기", "지갑/가방", "학생증/신분증", "기타"])
        with f_col2:
            start_date = st.date_input("시작날짜", value=None)
        with f_col3:
            end_date = st.date_input("종료날짜", value=None)
        with f_col4:
            st.write("") # 정렬용 여백
            apply_filter = st.button("필터적용", use_container_width=True)
        with f_col5:
            st.write("")
            reset_filter = st.button("초기화", use_container_width=True)

    st.markdown("---")

    # 3. 검색 결과 목록 영역 (와이어프레임 형태 반영)
    st.markdown("### 📋 검색 결과")
    
    # 데이터 조회 (검색어 또는 필터 적용)
    items = search_items(keyword=keyword, category=category, start_date=start_date, end_date=end_date)

    if not items:
        st.info("검색된 분실물이 없습니다.")
    else:
        for item in items:
            item_id, name, location, lost_date = item
            
            with st.container(border=True):
                col_img, col_info, col_action = st.columns([1, 4, 1])
                
                with col_img:
                    # 사진 영역 대체 박스
                    st.markdown(
                        """
                        <div style="background-color: #d3d3d3; height: 80px; display: flex; align-items: center; justify-content: center; border-radius: 5px; font-weight: bold; color: #555;">
                            사진
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                with col_info:
                    st.markdown(f"### {name}")
                    st.write(f"• 장소: {location or '미입력'}")
                    st.write(f"• 날짜: {lost_date or '미입력'}")
                with col_action:
                    st.write("") # 여백
                    if st.button("상세", key=f"search_detail_{item_id}", use_container_width=True):
                        st.session_state["selected_item_id"] = item_id
                        st.success(f"'{name}' 상세 페이지로 이동합니다.")
