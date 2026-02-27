# 여행 나래 (Travel Narae)

> 대한민국 문화유산 여행 도우미 AI 챗봇 웹 애플리케이션

"나래"는 **날개**의 순우리말로, 여행에 날개를 달아준다는 의미를 담고 있습니다.

---

## 주요 기능

- **AI 챗봇 (기가차드)** -- LangGraph 기반 에이전트가 문화유산 정보, 날씨, 맛집/카페 등을 직접 검색하여 답변
- **문화유산 RAG 검색** -- 전국 17개 시도의 문화유산 데이터셋을 ChromaDB 벡터 DB로 구축, 유사도 기반 검색
- **날씨 조회** -- Kakao 지도 API(지역명 → 좌표 변환) + 기상청 단기예보 API 연동
- **네이버 검색 (MCP)** -- 네이버 웹/뉴스/블로그/카페/지식iN 검색을 MCP 프로토콜로 연동
- **커뮤니티 게시판** -- 게시글 CRUD, 댓글/대댓글, 좋아요, 공지사항, 알림 기능
- **문화유산 지도** -- 지역별 문화유산 위치를 지도에서 확인
- **여행지 추천** -- 한국관광공사 Tour API 기반 지역별 관광지 추천
- **회원 시스템** -- 회원가입/로그인, 프로필 관리, 비밀번호 재설정, 환영 이메일 발송
- **Discord 봇** -- "기가차드"를 호출하면 Discord에서도 동일한 AI 챗봇 사용 가능

---

## 기술 스택

| 구분 | 기술 |
|------|------|
| AI/LLM | LangGraph, LangChain, GPT-4.1, OpenAI Embeddings (`text-embedding-3-large`) |
| 벡터 DB | ChromaDB (전국 17개 시도 문화유산 데이터) |
| MCP | Naver Search MCP (`@isnow890/naver-search-mcp`) |
| 백엔드 | Django, SQLAlchemy, MySQL, bcrypt |
| 프론트엔드 | Django Templates, django-widget-tweaks |
| 외부 API | Kakao 지도 API, 기상청 단기예보 API, 한국관광공사 Tour API |
| 봇 | discord.py |
| 기타 | python-dotenv, Pydantic, requests |

---

## 프로젝트 구조

```
TravelNarae/
├── chat_agent.py          # LangGraph 기반 AI 에이전트 그래프 정의
├── system_prompt.py       # 기가차드 시스템 프롬프트
├── app.py                 # CLI 챗봇 인터페이스
├── discord_agent.py       # Discord 봇 인터페이스
├── auth.py                # 회원 인증 (SQLAlchemy + bcrypt)
├── create_engine.py       # DB 엔진 설정
│
├── llm_tools/
│   ├── retriever.py       # 문화유산 RAG 검색 도구
│   ├── get_weather.py     # 날씨 조회 도구 (Kakao + 기상청)
│   ├── naver_search.py    # 네이버 검색 MCP 도구
│   ├── google_places.py   # Google Places 도구
│   └── chat_history_manager.py
│
├── chatbot_web/           # Django 웹 애플리케이션
│   ├── main/              # 메인 앱 (챗봇, 게시판, 지도, 인증)
│   └── chatbot_web/       # Django 프로젝트 설정
│
├── dataset/               # 전국 17개 시도 문화유산 CSV 데이터셋
├── chroma_db/             # ChromaDB 벡터 저장소
└── requirements.txt
```

---

## 팀 정보

**SKN 13기 3.5차 5Team**

