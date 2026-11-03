<p align="center">
  <img src="docs/images/pknufinder_logo.png" alt="PKNU Finder 로고" width="120">
</p>

# PKNU Finder

부경대학교 학생들을 위한 **분실물·습득물 찾기 서비스**입니다.
잃어버린 물건을 찾고, 주운 물건의 주인을 찾아줄 수 있도록 돕습니다.

- 프론트엔드/서버: [Streamlit](https://streamlit.io/)
- 데이터베이스·인증·파일 저장: [Supabase](https://supabase.com/) (PostgreSQL, Auth, Storage)

## 예상 화면

![실행 화면](docs/images/demo.png)

> 위 이미지는 **완성 시 예상 화면(기획 목업)** 입니다. 현재 구현 상태는 아래 표를 참고하세요.

## 현재 구현 현황 (중간발표 기준)

| 기능 | 상태 | 설명 | 담당 |
|------|------|------|------|
| 로그인 / 회원가입 | 사용 가능 | 이메일 가입·로그인 (Google, GitHub 소셜 로그인 버튼 포함) | 이민범 |
| 회원 탈퇴 | 사용 가능 | 마이페이지에서 탈퇴 처리 (계정 비활성화) | 이민범 |
| 분실물/습득물 등록 | 사용 가능 | 제목, 유형, 카테고리, 장소, 날짜, 설명, 태그, 사진 등록 | 윤한희 |
| 분실물/습득물 검색 | 개발 중 | 키워드 검색 | 박유진 |
| 채팅 | 준비 중 | 습득자와 분실자의 1:1 채팅 | 김채윤 |
| 북마크 | 준비 중 | 관심 게시글 저장 | 이민범 |

## 설치와 실행 (Python 3.12 이상, 3.13에서 테스트)

### 1. 저장소 받기

```bash
git clone https://github.com/chaeyun-pknu/pknu-finder.git
cd pknu-finder
```

### 2. 가상환경 만들기 (권장)

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. Supabase 접속 정보 설정 (필수)

접속 정보는 보안상 저장소에 포함되어 있지 않습니다.
`.streamlit/secrets.toml.example` 파일을 복사해 `.streamlit/secrets.toml` 파일을 만들고 값을 채워 주세요.

```bash
# macOS / Linux
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# Windows (PowerShell)
Copy-Item .streamlit\secrets.toml.example .streamlit\secrets.toml
```

```toml
# .streamlit/secrets.toml
SUPABASE_URL = "https://<project-ref>.supabase.co"
SUPABASE_SERVICE_ROLE_KEY = "<service_role 키>"
SUPABASE_ANON_KEY = "<anon 키>"
SUPABASE_REDIRECT_URL = "http://localhost:8501"
```

| 항목 | 설명 | 확인 위치 |
|------|------|-----------|
| `SUPABASE_URL` | Supabase 프로젝트 주소 | Supabase Dashboard → Project Settings → API |
| `SUPABASE_SERVICE_ROLE_KEY` | 서버 전용 관리자 키 (게시글 저장, 회원 탈퇴 등에 사용) | 같은 화면의 `service_role` 키 |
| `SUPABASE_ANON_KEY` | 로그인·회원가입에 사용하는 공개 키 | 같은 화면의 `anon` 키 |
| `SUPABASE_REDIRECT_URL` | 소셜 로그인 후 돌아올 앱 주소 (로컬 실행 시 `http://localhost:8501`) | - |

> 값은 팀 프로젝트 담당자(개발 리드 이민범)에게 전달받아 입력하세요.
> ⚠️ `service_role` 키는 DB 전체 권한을 가진 비밀 키입니다. **GitHub에 올리거나 채팅·압축 파일로 공유하지 마세요.**
> `.streamlit/secrets.toml`은 `.gitignore`에 등록되어 있습니다.

### 5. 앱 실행

Streamlit 앱이므로 `python main.py`가 아니라 **`streamlit run`** 으로 실행해야 합니다.

```bash
streamlit run main.py
```

브라우저에서 http://localhost:8501 이 열리면 정상입니다. (자동으로 열리지 않으면 주소를 직접 입력하세요.)
```bash
python -m streamlit run main.py --server.port 8501
```

## 사용법 (데모 순서)

1. **회원가입**: 첫 화면의 `회원가입` 탭에서 닉네임, 이메일, 비밀번호(영문·숫자 포함 6자 이상)를 입력합니다.
2. **로그인**: `로그인` 탭에서 이메일과 비밀번호로 로그인합니다. 로그인하면 홈 화면과 왼쪽 메뉴가 표시됩니다.
3. **게시글 등록**: 왼쪽 메뉴 `분실물/습득물 등록`에서 분실물 또는 습득물을 선택하고 정보와 사진(jpg, jpeg, png)을 입력한 뒤 등록합니다.
4. **회원 탈퇴**: 왼쪽 메뉴 `마이페이지` 하단의 `회원 탈퇴`에서 동의에 체크한 뒤 탈퇴합니다.
   - 탈퇴하면 같은 계정으로 다시 로그인할 수 없습니다.
   - 기존 게시글은 유지되고, 작성자 이름은 `탈퇴한 유저_xxxxxxxx` 형태로 바뀝니다.
5. **로그아웃**: 왼쪽 사이드바의 `로그아웃` 버튼을 누릅니다.

## Supabase 설정

팀에서 사용 중인 Supabase 프로젝트의 접속 정보를 받았다면 아래 설정은 이미 완료되어 있습니다.
**새 Supabase 프로젝트에서 직접 구성하는 경우**에만 따라 해 주세요.

- 프로젝트·테이블·Storage 생성 방법은 [DB/database.md](DB/database.md)를 따릅니다.
- 현재 코드는 `DB/database.md`의 테이블 정의에 더해 아래 컬럼이 필요합니다. SQL Editor에서 한 번 실행해 주세요.

  ```sql
  -- 회원 탈퇴 처리용 컬럼
  ALTER TABLE public.users
      ADD COLUMN IF NOT EXISTS is_deleted BOOLEAN DEFAULT FALSE,
      ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMPTZ;

  -- 게시글 태그 저장용 컬럼
  ALTER TABLE public.lost_items
      ADD COLUMN IF NOT EXISTS tags TEXT[] DEFAULT '{}';
  ```

- Storage에 `lost-item-images` Bucket(Private)이 있어야 사진 등록이 됩니다.
- **Authentication → URL Configuration**
  - Site URL: `http://localhost:8501`
  - Redirect URLs: `http://localhost:8501/**`
- **Authentication → Providers**: Email을 켭니다. Google, GitHub 소셜 로그인을 쓰려면 각 Provider도 설정해야 합니다.
- 데모에서 가입 직후 바로 로그인되게 하려면 Email Provider의 **Confirm email** 옵션을 끄세요. 켜져 있으면 가입 후 메일 인증을 해야 로그인할 수 있습니다.

## 문제 해결

| 증상 | 확인할 것 |
|------|-----------|
| `Supabase 연결 설정이 필요합니다` 화면 | `.streamlit/secrets.toml` 파일이 있는지, `SUPABASE_URL`과 키 값이 채워져 있는지 확인 |
| `Supabase 데이터베이스를 확인하지 못했습니다` | `users` 테이블이 있는지, 키가 올바른지 확인 |
| `streamlit: command not found` | 가상환경이 활성화되어 있는지, `pip install -r requirements.txt`를 했는지 확인 (또는 `python -m streamlit run main.py`) |
| 게시글 등록 시 컬럼 오류 (`tags` 등) | 위 `Supabase 설정`의 `ALTER TABLE` SQL 실행 여부 확인 |
| 사진 등록 오류 | Storage에 `lost-item-images` Bucket이 있는지 확인 |
| 소셜 로그인 후 오류 | Supabase `Redirect URLs`에 `http://localhost:8501/**`가 등록되어 있는지, `SUPABASE_REDIRECT_URL`이 실행 주소와 같은지 확인 |
| 회원가입 후 로그인이 안 됨 | `Confirm email` 옵션이 켜져 있다면 메일 인증 후 로그인 |
| `8501` 포트가 이미 사용 중 | `streamlit run main.py --server.port 8502` 로 실행하고 `SUPABASE_REDIRECT_URL`도 같은 포트로 변경 |

## 프로젝트 구조

```text
pknu-finder/
├── main.py                  # 앱 진입점 (streamlit run main.py)
├── requirements.txt
├── .streamlit/
│   ├── secrets.toml.example # 접속 정보 예시 (복사해서 secrets.toml로 사용)
│   └── secrets.toml         # 실제 접속 정보 (Git 제외)
├── DB/
│   ├── database.py          # Supabase 연결 모듈
│   ├── database.md          # Supabase 설정 가이드
│   └── DB_use_guide.md      # Python에서 DB 사용하는 방법
├── views/
│   ├── home/                # 홈 화면
│   ├── register/            # 분실물/습득물 등록
│   ├── search/              # 분실물/습득물 검색
│   ├── chat/                # 채팅 (준비 중)
│   └── mypage/              # 로그인·회원가입·회원 탈퇴·마이페이지
└── docs/                    # 이미지, 회의록, 팀 문서
```

## 팀원

| 이름 | 역할 | GitHub |
|------|------|--------|
| 김채윤 | 팀장 | chaeyun-pknu |
| 이민범 | 개발 리드 | alsqja03 |
| 박유진 | 문서 담당 | yujinsutu |
| 윤한희 | 리뷰.품질 담당 | yoonhanhee |

기여 방법은 [CONTRIBUTING.md](CONTRIBUTING.md), 행동 수칙은 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
를 참고하세요.

## 라이선스

MIT License — see [LICENSE](LICENSE)
