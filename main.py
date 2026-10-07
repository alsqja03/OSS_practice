import streamlit as st

# === 유저 로그인 상태 관리 간단 구현 ===
if "login" not in st.session_state:
    st.session_state.login = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "keyword" not in st.session_state:
    st.session_state.keyword = ""

# === 사이드바 메뉴 리스트 ===
menu_list = ["홈", "분실물 등록", "채팅", "마이페이지"]

def main():
    # 사이드바 구성
    with st.sidebar:
        st.markdown(
            """
            <h1 style="font-weight:bold;">PKNU FINDER</h1>
            """,
            unsafe_allow_html=True,
        )

        # 메뉴 선택
        menu_choice = st.radio("", menu_list)

        # 하단 부경대학교 로고 (임시 텍스트 대신 이미지 사용 가능)
        st.markdown("<div style='position:absolute; bottom:20px; width:90%;'>"
                    "<img src='https://upload.wikimedia.org/wikipedia/commons/8/8f/Pukyong_National_University_Logo.svg' alt='부경대학교 로고' style='width:100%; max-width:150px;'/></div>",
                    unsafe_allow_html=True)

    # 상단 우측에 로그인/회원가입 또는 로그아웃 버튼 배치
    login_col1, login_col2 = st.columns([9, 1])
    with login_col2:
        if st.session_state.login:
            if st.button("로그아웃"):
                st.session_state.login = False
                st.session_state.user_id = None
                st.experimental_rerun()
        else:
            if st.button("회원가입/로그인"):
                # 회원가입/로그인 페이지 (본 예제는 간단히 로그인만 구현)
                login_page()
                return

    # 메뉴별 화면 이동
    if menu_choice == "홈":
        home_page()
    elif menu_choice == "분실물 등록":
        if not st.session_state.login:
            login_page()
        else:
            lost_registration_page()
    elif menu_choice == "채팅":
        if not st.session_state.login:
            login_page()
        else:
            chat_page()
    elif menu_choice == "마이페이지":
        if not st.session_state.login:
            login_page()
        else:
            mypage()

# 메인 화면 (홈)
def home_page():
    st.title("PKNU FINDER에 오신 것을 환영합니다!")
    st.write("분실물을 검색하고, 주인을 찾아주세요.")

    # 검색창 (키워드 유지)
    keyword = st.text_input("물건 이름, 장소, 키워드를 입력하세요.", st.session_state.keyword)
    if st.button("검색"):
        st.session_state.keyword = keyword
        search_page(keyword)

    # 최근 등록된 분실물 예시 (더미 데이터)
    st.subheader("최근 등록된 분실물들")
    recent_items = [
        {"name": "검은색 카드지갑", "location": "중앙도서관", "date": "2026.09.28"},
        {"name": "에어팟 (1세대)", "location": "학생회관", "date": "2026.09.27"},
        {"name": "검은색 우산", "location": "공학관", "date": "2026.09.26"},
    ]

    cols = st.columns(len(recent_items))
    for idx, item in enumerate(recent_items):
        with cols[idx]:
            st.image("https://via.placeholder.com/150", width=120)  # 임시 이미지
            st.write(f"**{item['name']}**")
            st.write(item["location"])
            st.write(item["date"])

    if st.button("전체보기"):
        st.session_state.keyword = ""
        lost_items_page()

# 검색 결과 페이지
def search_page(keyword):
    st.title(f'검색 결과 : "{keyword}"')
    # 예시 검색 결과 (더미 데이터)
    # 실제 DB나 API 적용시 여기서 데이터 필터링 후 보여주면 됨.
    search_results = [
        {"name": "검은색 카드지갑", "location": "중앙도서관", "date": "2026.09.28"},
        {"name": "갈색 반지갑", "location": "학생회관", "date": "2026.09.27"},
        {"name": "네이비 지갑", "location": "공학관", "date": "2026.09.25"},
        {"name": "검정 카드지갑 (로고 있음)", "location": "도서관 앞", "date": "2026.09.24"},
        {"name": "초록색 지갑", "location": "기숙사 앞", "date": "2026.09.22"},
    ]

    filtered_results = [res for res in search_results if keyword.lower() in res["name"].lower()]
    if not filtered_results:
        st.write("검색 결과가 없습니다.")
        return

    for item in filtered_results:
        st.write(f"**{item['name']}**  -  {item['location']}  -  {item['date']}  ")
        if st.button(f"상세보기 - {item['name']}"):
            lost_detail_page(item)
            return

# 분실물 전체보기 페이지
def lost_items_page():
    st.title("전체 분실물 목록")
    # 실제 데이터 대체 필요
    items = [
        {"name": "검은색 카드지갑", "location": "중앙도서관", "date": "2026.09.28"},
        {"name": "에어팟 (1세대)", "location": "학생회관", "date": "2026.09.27"},
        {"name": "검은색 우산", "location": "공학관", "date": "2026.09.26"},
        # 추가 분실물...
    ]
    for item in items:
        st.write(f"**{item['name']}**  -  {item['location']}  -  {item['date']}")
        if st.button(f"상세보기 - {item['name']}"):
            lost_detail_page(item)
            return

# 분실물 상세 페이지
def lost_detail_page(item):
    st.title(item["name"])
    st.write(f"분실 위치: {item['location']}")
    st.write(f"등록일: {item['date']}")
    st.image("https://via.placeholder.com/300")  # 이미지 자리

    if st.button("채팅하기"):
        if not st.session_state.login:
            login_page()
        else:
            chat_with_item(item)

# 분실물 등록 페이지
def lost_registration_page():
    st.title("분실물 등록")

    name = st.text_input("물건 이름")
    location = st.text_input("분실 위치")
    date = st.date_input("분실 날짜")
    register_btn = st.button("등록")

    if register_btn:
        # 실제 등록 DB or API 호출 부분
        st.success("분실물이 등록되었습니다!")
        st.experimental_rerun()

# 채팅 리스트 페이지 (간략)
def chat_page():
    st.title("내 채팅 리스트")
    # 예시 데이터 (실제 데이터 연결 필요)
    chats = [
        {"with": "검은색 카드지갑", "last_msg": "연락주세요", "date": "2026.09.28"},
        # 추가 채팅방...
    ]

    for c in chats:
        st.write(f"{c['with']} - {c['last_msg']} ({c['date']})")
        if st.button(f"{c['with']} 채팅방 입장"):
            chat_with_item({"name": c["with"]})
            return

# 채팅 화면 예시
def chat_with_item(item):
    st.title(f"{item['name']} 와의 채팅")
    # 대화창, 메시징 등은 실제 구현 필요 (여기선 최소 UI만)
    chat_input = st.text_input("메시지 입력...")
    if st.button("보내기"):
        st.success("메시지가 전송되었습니다.")

# 마이페이지
def mypage():
    st.title("마이페이지")
    st.write(f"환영합니다, {st.session_state.user_id}님!")

# 로그인 페이지 (간단 구현)
def login_page():
    st.title("로그인")
    user = st.text_input("아이디")
    pwd = st.text_input("비밀번호", type="password")
    if st.button("로그인"):
        # 간단 로그인 예제, 실제는 DB 연동 필요
        if user == "user" and pwd == "1234":
            st.session_state.login = True
            st.session_state.user_id = user
            st.success("로그인 성공!")
            st.experimental_rerun()
        else:
            st.error("아이디 또는 비밀번호가 잘못되었습니다.")

if __name__ == "__main__":
    main()
