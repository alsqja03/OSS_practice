import streamlit as st
from datetime import date
from database import get_connection


def register_item(name, location, lost_date, user_id, description=""):
    """새로운 분실물/습득물 정보를 DB에 저장합니다."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO lost_items (name, location, lost_date, user_id)
            VALUES (?, ?, ?, ?)
            """,
            (name, location, str(lost_date), user_id),
        )
        conn.commit()
        return True


def render_registration():
    st.title("📝 분실물 / 습득물 등록")

    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("로그인 후 이용할 수 있는 서비스입니다.")
        return

    with st.container(border=True):
        col_left, col_right = st.columns([1, 1])

        with col_left:
            # 사진 추가 영역
            st.markdown(
                """
                <div style="background-color: #b0b0b0; height: 220px; display: flex; align-items: center; justify-content: center; border-radius: 5px; font-size: 20px; font-weight: bold; color: white; position: relative;">
                    사진
                </div>
                """,
                unsafe_allow_html=True
            )
            uploaded_file = st.file_uploader("이미지 업로드", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
            st.button("추가", use_container_width=True)

        with col_right:
            item_name = st.text_input("제목", placeholder="제목을 입력하세요", label_visibility="collapsed")
            location = st.text_input("장소", placeholder="장소를 입력하세요", label_visibility="collapsed")
            lost_date = st.date_input("날짜", value=date.today(), label_visibility="collapsed")
            item_type = st.selectbox("구분", ["습득물", "분실물"], label_visibility="collapsed")

    # 목록 태그 영역
    st.markdown("#### 목록 태그")
    tags = st.text_input("태그 입력", placeholder="예) #지갑, #도서관", label_visibility="collapsed")

    # 설명 영역
    st.markdown("#### 설명")
    description = st.text_area("상세 설명", placeholder="상세 설명을 입력하시오", label_visibility="collapsed", height=120)

    st.markdown("---")

    # 등록하기 버튼
    if st.button("등록 완료", type="primary", use_container_width=True):
        if not item_name:
            st.error("제목(물품명)을 입력해주세요.")
        else:
            success = register_item(
                name=f"[{item_type}] {item_name} (태그: {tags})", 
                location=location, 
                lost_date=lost_date, 
                user_id=user_id,
                description=description
            )
            if success:
                st.success("분실물/습득물이 성공적으로 등록되었습니다!")
            else:
                st.error("등록 중 오류가 발생했습니다.")
