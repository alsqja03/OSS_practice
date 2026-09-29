import streamlit as st

# 1. 페이지 기본 설정 (와이드 레이아웃 적용)
st.set_page_config(
    page_title="PKNU FINDER", 
    page_icon="🔍", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 커스텀 CSS 적용 (카드 UI 및 전체적인 여백 디자인)
st.markdown("""
    <style>
    /* 메인 컨테이너 상단 여백 줄이기 */
    .block-container {
        padding-top: 2rem;
    }
    
    /* 웰컴 배너 스타일 */
    .welcome-banner {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 40px;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    
    /* 분실물 카드 스타일 */
    .item-card {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px;
        background-color: white;
        transition: transform 0.2s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .item-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    
    /* 사이드바 하단 로고용 여백 */
    .sidebar-footer {
        position: absolute;
        bottom: 20px;
        width: 100%;
        text-align: center;
        color: #888;
        font-size: 12px;
    }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 📌 사이드바 (Navigation)
# ==========================================
with st.sidebar:
    st.markdown("### 🔍 PKNU FINDER")
    st.caption("분실물, 다시 만날 수 있도록")
    st.markdown("---")
    
    # 메뉴 선택 (라디오 버튼을 메뉴처럼 스타일링)
    menu = st.radio(
        "메뉴", 
        ["🏠 홈", "📝 분실물 등록", "💬 내 채팅", "👤 마이페이지"],
        label_visibility="collapsed"
    )
    
    st.markdown("<br>" * 15, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**🔵 부경대학교**<br><span style='font-size: 0.8em; color: gray;'>함께하는 더 좋은 캠퍼스</span>", unsafe_allow_html=True)


# ==========================================
# 📌 메인 화면 (홈)
# ==========================================
if menu == "🏠 홈":
    
    # 1. 상단 웰컴 배너 영역
    st.markdown("""
        <div class="welcome-banner">
            <h2 style="color: #0d47a1; margin-top: 0;">PKNU FINDER에 오신 것을 환영합니다!</h2>
            <p style="color: #424242; font-size: 16px;">분실물을 검색하고, 주인을 찾아주세요.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 2. 검색창 영역
    search_col1, search_col2 = st.columns([5, 1])
    with search_col1:
        search_query = st.text_input(
            "검색창", 
            placeholder="🔍 물건 이름, 장소, 키워드로 검색해보세요.", 
            label_visibility="collapsed"
        )
    with search_col2:
        # 버튼을 텍스트 인풋과 높이를 맞추기 위해 마진 적용
        st.button("검색", type="primary", use_container_width=True)
        
    st.markdown("<br>", unsafe_allow_html=True)

    # 3. 최근 등록된 분실물 헤더 영역
    header_col1, header_col2 = st.columns([4, 1])
    with header_col1:
        st.subheader("최근 등록된 분실물")
    with header_col2:
        st.markdown("<div style='text-align: right; padding-top: 10px; color: gray; cursor: pointer;'>전체보기 ></div>", unsafe_allow_html=True)

    # 4. 아이템 카드 목록 (3열 그리드)
    # 실제 개발 시에는 반복문(for)과 DB 데이터를 사용하여 동적으로 생성합니다.
    col1, col2, col3 = st.columns(3)
    
    # 샘플 데이터 (디자인 초안 1번 패널 기준)
    items = [
        {"name": "검은색 카드지갑", "loc": "중앙도서관", "date": "2026.09.28", "img": "https://images.unsplash.com/photo-1627123424574-724758594e93?w=300&q=80"},
        {"name": "에어팟 (1세대)", "loc": "학생회관", "date": "2026.09.27", "img": "https://images.unsplash.com/photo-1606220588913-b3aacb4d2f46?w=300&q=80"},
        {"name": "검은색 우산", "loc": "공학관", "date": "2026.09.26", "img": "https://images.unsplash.com/photo-1559281699-2475b1c97a58?w=300&q=80"}
    ]
    
    # 카드 1
    with col1:
        st.markdown('<div class="item-card">', unsafe_allow_html=True)
        st.image(items[0]["img"], use_column_width=True)
        st.markdown(f"**{items[0]['name']}**")
        st.caption(f"📍 {items[0]['loc']}<br>📅 {items[0]['date']}", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 카드 2
    with col2:
        st.markdown('<div class="item-card">', unsafe_allow_html=True)
        st.image(items[1]["img"], use_column_width=True)
        st.markdown(f"**{items[1]['name']}**")
        st.caption(f"📍 {items[1]['loc']}<br>📅 {items[1]['date']}", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 카드 3
    with col3:
        st.markdown('<div class="item-card">', unsafe_allow_html=True)
        st.image(items[2]["img"], use_column_width=True)
        st.markdown(f"**{items[2]['name']}**")
        st.caption(f"📍 {items[2]['loc']}<br>📅 {items[2]['date']}", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # 다른 메뉴 클릭 시 표시될 화면 (더미)
    st.title(menu)
    st.write(f"현재 선택된 메뉴는 **{menu}** 입니다. 해당 기능 개발을 진행해 주세요.")
