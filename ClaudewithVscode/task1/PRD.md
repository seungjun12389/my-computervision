# PRD: 이한양 개인 포트폴리오 웹사이트

- **문서 버전**: v1.0
- **작성일**: 2026-09-08
- **대상 서비스**: 개인 포트폴리오 웹사이트 (1인, 정적 사이트)
- **원본 자료**: `resume_sample.docx`

---

## 1. 개요 (Overview)

졸업을 앞둔 인공지능학과 학부생이 **채용 담당자와 현직 엔지니어에게 자신을 소개하고 프로젝트 역량을 증명**하기 위한 개인 포트폴리오 웹사이트를 만든다. 이력서(`resume_sample.docx`)의 내용을 빠짐없이 웹으로 옮기되, PDF 이력서보다 **빠르게 훑고 깊게 파고들 수 있는** 형태로 재구성한다.

### 1.1 문제 정의
- 채용 담당자는 지원자 1명당 30초~1분만 사용한다. PDF 이력서는 링크 클릭과 프로젝트 탐색이 불편하다.
- GitHub 저장소만으로는 프로젝트의 **문제 정의 → 접근 → 결과** 흐름이 드러나지 않는다.
- 신입 AI 엔지니어 지원자 사이에서 "PyTorch를 다룰 수 있다"는 차별점이 되지 못한다. **AI 시스템 전 과정을 직접 구현해봤다**는 근거를 보여줘야 한다.

### 1.2 해결 방안
한 페이지 스크롤 기반의 정적 웹사이트를 만든다. 상단 5초 안에 "누구인지"를 각인시키고, 아래로 내려가며 학력 · 활동 · 기술 · 프로젝트를 근거로 제시한다. 모든 프로젝트는 GitHub 링크로 즉시 연결된다.

---

## 2. 목표 (Goals)

### 2.1 사용자 목표

| 대상 | 목표 |
|---|---|
| 채용 담당자 / 리크루터 | 30초 안에 전공 · 기술 스택 · 대표 프로젝트를 파악하고 연락처를 확보한다 |
| 현직 AI 엔지니어 (면접관) | 프로젝트의 기술적 깊이(RAG 파이프라인 설계, Transfer Learning 적용)를 확인하고 GitHub 코드로 이동한다 |
| 본인 (사이트 소유자) | URL 하나로 자기소개를 대체하고, 새 프로젝트가 생길 때 쉽게 추가한다 |

### 2.2 성공 지표 (Success Metrics)

| 지표 | 목표치 |
|---|---|
| 첫 화면 로딩 (LCP) | 2.0초 이내 |
| GitHub 링크 클릭률 | 방문자의 30% 이상 |
| 이메일 복사 · 클릭 | 방문자의 10% 이상 |
| 모바일 이탈률 | 60% 이하 |
| Lighthouse 성능 / 접근성 / SEO | 각 90점 이상 |

### 2.3 비목표 (Non-Goals)
- 블로그 · 게시판 등 콘텐츠 관리 기능 (v1 제외)
- 로그인, 회원가입, 방문자 댓글
- 다국어 지원 (v1은 한국어 단일, 영문은 v2 후보)
- 백엔드 서버 및 데이터베이스 (정적 사이트로 충분)

---

## 3. 타깃 사용자 (Target Users)

**Primary — 인사담당자 (IT 기업, 30대 초반)**
- 신입 AI 엔지니어 공고에 지원한 이력서 수십 건을 검토 중이다.
- 노트북 브라우저로 지원자가 첨부한 포트폴리오 링크를 연다.
- 필요 정보: 학력, 졸업 예정 시기, 기술 스택, 프로젝트 유무, 연락처.
- 이탈 요인: 로딩이 느림, 스크롤을 많이 해야 스택이 나옴, 연락처를 찾기 어려움.

**Secondary — AI 팀 리드 (면접관, 30대 후반)**
- 면접 전 지원자의 프로젝트를 훑어본다.
- 필요 정보: 프로젝트에서 **본인이 맡은 역할**, 기술 선택의 이유, 성능 개선 시도(Chunk Size · Top-K 비교 등), 코드 품질.
- 이탈 요인: 프로젝트 설명이 "~했습니다" 나열뿐이고 결과와 수치가 없을 때.

**Tertiary — 모바일 방문자**
- 링크드인 · 카카오톡으로 공유받아 스마트폰에서 연다. 전체 트래픽의 40% 이상으로 가정한다.

---

## 4. 정보 구조 (Information Architecture)

단일 페이지(One-page) 스크롤 구조 + 상단 고정 내비게이션(앵커 이동).

```
┌─ Header (fixed nav) ──────────────────────────────────┐
│  이한양 │ About  Education  Skills  Projects  Contact  │
└───────────────────────────────────────────────────────┘
  │
  ├─ 1. Hero         이름 + AI ENGINEER + 한 줄 요약 + CTA
  ├─ 2. About        자기소개 (이력서 요약문 기반)
  ├─ 3. Education    학력 + 관련 과목
  ├─ 4. Activities   AI 학술동아리, AI Summer Study
  ├─ 5. Skills       언어 / AI·ML / Tools 3분류
  ├─ 6. Projects     프로젝트 카드 2건  ← 핵심 섹션
  ├─ 7. Contact      GitHub, E-mail, Phone
  └─ Footer          © 2026 이한양
```

---

## 5. 기능 요구사항 (Functional Requirements)

### FR-1. Hero 섹션 — 필수
- 이름 **이한양**과 직무 타이틀 **AI ENGINEER**를 대비되는 크기로 배치한다.
- 한 줄 포지셔닝 문구: "데이터 전처리부터 모델 학습, 서비스 구현까지 AI 시스템의 전 과정을 직접 만드는 엔지니어".
- CTA 버튼 2개: `프로젝트 보기`(#projects 앵커 이동), `GitHub`(새 탭).
- 진입 시 페이드인 애니메이션. `prefers-reduced-motion` 설정을 존중한다.

### FR-2. About 섹션 — 필수
- 이력서 상단 요약문을 2~3문단으로 재구성해 표시한다.
- 강조 키워드(PyTorch, Transformer, NLP, LLM, RAG)를 시각적으로 하이라이트한다.

### FR-3. Education 섹션 — 필수
- 표시 항목: `2023.03 – 현재 · 한양대학교 인공지능학과 학사과정`
- 하위 정보: 2026년 현재 4학년 재학 / 학점(전공) 3.0 · 4.5
- 관련 과목 8개(인공지능, 머신러닝, 딥러닝, 자연어처리, 컴퓨터비전, 자료구조, 알고리즘, 확률 및 통계)를 태그(pill) 형태로 나열한다.

### FR-4. Activities 섹션 — 필수
타임라인 형태로 2건을 시간 역순으로 표시한다. 각 항목은 `기간 · 기관 · 제목 · 불릿 설명` 구조를 따른다.

1. **2025.03 – 2025.12 · 한양대학교 인공지능학과 AI 학술동아리**
   - 머신러닝 · 딥러닝 논문 및 기술 스터디
   - PyTorch를 활용한 CNN, RNN, Transformer 모델 구현
   - Hugging Face 기반 사전학습 모델 Fine-tuning 실습
2. **2025.07 – 2025.08 · 교내 AI Summer Study (생성형 AI & LLM 스터디)**
   - Transformer 및 LLM 구조 학습
   - Prompt Engineering 및 RAG 구조 실습
   - LangChain을 활용한 LLM Application 개발

### FR-5. Skills 섹션 — 필수
3개 카테고리로 그룹핑하여 배지 형태로 표시한다.

| 카테고리 | 항목 |
|---|---|
| Programming Language | Python, C++ |
| AI / ML | PyTorch, Scikit-Learn, Hugging Face Transformers, NLP, Computer Vision, LLM, RAG |
| Tools | Git, GitHub, Docker, FastAPI, Streamlit, Jupyter Notebook |

- (선택, v1.1 후보) 배지 클릭 시 해당 기술을 사용한 프로젝트 카드를 강조하는 필터 기능.

### FR-6. Projects 섹션 — 핵심 · 필수
카드형 레이아웃. 모든 카드는 아래 구조를 동일하게 갖는다.

`기간 / 유형(팀·개인) 뱃지` → `프로젝트명` → `한 줄 요약` → `상세 불릿 3~5개` → `Tech Stack 배지` → `GitHub 링크 버튼(새 탭, rel="noopener noreferrer")`

**Project 1 — 한양대 학사정보 RAG 챗봇** (2026.03 – 2026.05, 팀 프로젝트)
- 요약: 한양대학교 학사 안내 문서와 학과 정보를 검색하여 질문에 답변하는 RAG 기반 챗봇
- 학사 공지 및 PDF 문서를 Chunk 단위로 분할하고 Embedding하여 Vector DB에 저장
- 질문과 관련된 문서를 검색한 뒤 LLM이 해당 문서를 근거로 답변하도록 RAG Pipeline 구현
- 검색 정확도 개선을 위해 Chunk Size 및 Top-K 값에 따른 성능 비교
- FastAPI와 Streamlit을 활용한 웹 기반 데모 구현
- Tech Stack: Python, LangChain, Hugging Face, FAISS, FastAPI, Streamlit
- GitHub: https://github.com/example-hanyang-ai/hyu-rag-chatbot

**Project 2 — 딥러닝 기반 음식 이미지 분류 및 영양정보 추천 시스템** (2025.09 – 2025.12, 팀 프로젝트)
- 요약: 음식 이미지를 입력받아 종류를 분류하고 관련 영양정보를 제공하는 AI 서비스
- 공개 음식 이미지 데이터셋을 활용한 데이터 전처리 및 Augmentation 수행
- ResNet 기반 Transfer Learning을 적용하여 이미지 분류 모델 구축
- Accuracy, Precision, Recall, F1-score를 활용한 모델 성능 평가
- 학습된 모델을 API 형태로 구성하고 웹 인터페이스에서 이미지 업로드 및 추론 가능하도록 구현
- Tech Stack: Python, PyTorch, torchvision, ResNet, FastAPI, Streamlit
- GitHub: https://github.com/example-hanyang-ai/food-vision-demo

### FR-7. Contact 섹션 — 필수
- GitHub: https://github.com/example-hanyang-ai (새 탭)
- E-mail: lee.hanyang@example.com — `mailto:` 링크 + 클립보드 복사 버튼(복사 시 "복사되었습니다" 토스트)
- Phone: 010-0000-0000 — 모바일에서 `tel:` 링크로 동작
- 스팸 수집 방지를 위해 이메일 주소는 JS 조합 등 최소한의 난독화를 적용한다.

### FR-8. 내비게이션 — 필수
- 상단 고정(sticky) 헤더, 스크롤 시 배경 블러 · 그림자 적용.
- 현재 보고 있는 섹션의 메뉴를 활성 표시(IntersectionObserver 기반 scroll-spy).
- 모바일에서는 햄버거 메뉴로 전환.
- 앵커 이동 시 부드러운 스크롤, 고정 헤더 높이만큼 오프셋을 보정한다.

### FR-9. 다크 모드 — 권장
- 시스템 설정(`prefers-color-scheme`) 자동 감지 + 수동 토글 버튼.
- 선택값을 `localStorage`에 저장하여 재방문 시 유지한다.

### FR-10. 이력서 다운로드 — 선택 (v1.1)
- 원본 PDF 이력서 다운로드 버튼을 Hero 또는 Contact에 배치한다.

---

## 6. 비기능 요구사항 (Non-Functional Requirements)

### 6.1 성능
- 페이지 전체 용량 1MB 이하, 이미지는 WebP 사용 및 `loading="lazy"` 적용.
- 웹폰트는 필요한 굵기만 서브셋 로드하고 `font-display: swap`을 지정한다.

### 6.2 반응형

| 브레이크포인트 | 레이아웃 |
|---|---|
| ~ 767px (모바일) | 1단, 햄버거 메뉴, 프로젝트 카드 세로 스택 |
| 768 ~ 1023px (태블릿) | 1~2단 혼합 |
| 1024px ~ (데스크톱) | 콘텐츠 최대 폭 1120px 중앙 정렬, 프로젝트 2단 |

### 6.3 접근성 (a11y)
- 시맨틱 태그(`header`, `nav`, `main`, `section`, `article`, `footer`)를 사용한다.
- 본문 텍스트 명도 대비 4.5:1 이상을 라이트 · 다크 모드 모두에서 만족한다.
- 모든 인터랙티브 요소는 키보드로 접근 가능하며 `:focus-visible`로 포커스를 표시한다.
- 이미지에 `alt`, 아이콘 전용 버튼에 `aria-label`을 반드시 지정한다.
- `prefers-reduced-motion: reduce`일 때 애니메이션을 비활성화한다.

### 6.4 브라우저 지원
- Chrome, Edge, Safari, Firefox 최신 2개 버전 / iOS Safari, Android Chrome. IE 미지원.

### 6.5 SEO 및 공유
- `<title>`: "이한양 | AI Engineer 포트폴리오"
- `<meta name="description">`: 자기소개 요약 150자 이내.
- Open Graph / Twitter Card 태그와 OG 이미지(1200×630) 설정 — 카카오톡 · 링크드인 공유 시 카드 노출.
- `robots.txt`, `sitemap.xml` 포함. JSON-LD `Person` 스키마 적용을 권장한다.

### 6.6 개인정보
- 전화번호 노출 여부를 설정 상수 하나로 켜고 끌 수 있어야 한다.

---

## 7. 디자인 방향 (Design Direction)

- **톤앤매너**: 절제된 테크 감성. 화려한 그래픽보다 여백과 타이포그래피 중심으로 신뢰감을 준다.
- **컬러**: 중성 배경(라이트 `#FAFAFA` / 다크 `#0E1116`) + 포인트 컬러 1개(딥 블루 또는 시안 계열). 포인트 컬러는 CTA · 활성 메뉴 · 강조 키워드에만 사용한다.
- **타이포그래피**: 국문 Pretendard, 영문 · 코드 Inter 또는 JetBrains Mono. 본문 16px, 행간 1.7.
- **레이아웃**: 섹션 상하 여백 96px(데스크톱) / 64px(모바일), 콘텐츠 최대 폭 1120px.
- **모션**: 스크롤 진입 시 8~16px 상승 + 페이드인, 200~300ms. 과하지 않게 한다.

---

## 8. 기술 스택 (Tech Stack)

| 항목 | 선택 | 근거 |
|---|---|---|
| 구현 | HTML + CSS + Vanilla JavaScript (정적) | 콘텐츠가 고정적이고 페이지가 1개이므로 프레임워크가 불필요하다. 로딩 속도와 유지보수에 유리하다 |
| 스타일 | CSS 커스텀 프로퍼티 기반 토큰 + Flexbox / Grid | 다크 모드 전환을 변수 교체만으로 처리할 수 있다 |
| 데이터 | `data.js`(또는 `data.json`)로 이력 내용 분리 | 프로젝트 추가 시 HTML을 건드리지 않고 데이터만 수정한다 |
| 배포 | GitHub Pages (대안: Vercel, Netlify) | 무료이고 GitHub 계정과 자연스럽게 연결되며 커스텀 도메인을 붙일 수 있다 |
| 분석 | Google Analytics 4 또는 Vercel Analytics (선택) | 2.2의 성공 지표 측정용 |

> 향후 블로그 · 다국어가 필요해지면 Next.js(App Router) + Vercel로 이전한다.

---

## 9. 콘텐츠 소스 매핑 (Content Mapping)

| 웹사이트 섹션 | 이력서 원본 위치 | 비고 |
|---|---|---|
| Hero | 이름 + `AI ENGINEER` | 한 줄 문구는 요약문에서 발췌 |
| About | 상단 자기소개 문단 | 문단 분리 및 키워드 강조 |
| Education | EDUCATION | 관련 과목을 태그로 변환 |
| Activities | ACTIVITIES | 타임라인 UI |
| Skills | SKILLS | 3개 카테고리 유지 |
| Projects | PROJECTS | 카드 2건, Tech Stack · GitHub 링크 포함 |
| Contact | CONTACT | 이메일 복사 기능 추가 |

---

## 10. 개발 범위 및 마일스톤 (Scope & Milestones)

| 단계 | 내용 | 산출물 |
|---|---|---|
| M1. 셋업 | 프로젝트 구조 생성, 디자인 토큰(색 · 타이포 · 간격) 정의, `data.js` 작성 | 폴더 구조, 콘텐츠 데이터 |
| M2. 마크업 | 전 섹션 시맨틱 HTML + 데스크톱 스타일 | 정적 페이지 초안 |
| M3. 반응형 | 모바일 · 태블릿 대응, 햄버거 메뉴 | 반응형 완료 |
| M4. 인터랙션 | scroll-spy, 스무스 스크롤, 다크 모드, 이메일 복사, 스크롤 애니메이션 | 기능 완료 |
| M5. 품질 | Lighthouse 점검, 명도 대비 · 키보드 내비게이션 검증, 크로스 브라우저 확인 | 90점 이상 |
| M6. 배포 | OG 태그 · 파비콘 · `sitemap.xml` 추가, GitHub Pages 배포 | 공개 URL |

---

## 11. 파일 구조 (제안)

```
task1/
├── index.html
├── assets/
│   ├── css/style.css
│   ├── js/main.js          # nav, scroll-spy, theme, copy
│   ├── js/data.js          # 이력 콘텐츠 데이터
│   ├── img/og-image.png
│   └── img/favicon.svg
├── resume.pdf              # (선택) 다운로드용
├── robots.txt
├── sitemap.xml
└── PRD.md
```

---

## 12. 완료 조건 (Acceptance Criteria)

- [ ] `resume_sample.docx`의 모든 항목(요약, Contact, Education, Activities, Skills, Projects 2건)이 누락 없이 반영되어 있다.
- [ ] 모바일(360px) · 태블릿(768px) · 데스크톱(1440px)에서 가로 스크롤이 발생하지 않고 레이아웃이 깨지지 않는다.
- [ ] 상단 내비게이션의 모든 앵커가 정확한 섹션으로 이동하며, 현재 섹션이 활성 표시된다.
- [ ] 모든 외부 링크(GitHub 3개)가 새 탭에서 정상 동작한다.
- [ ] 이메일 복사 버튼이 동작하고 피드백 메시지가 노출된다.
- [ ] 다크 모드 토글이 동작하고 새로고침 후에도 선택이 유지된다.
- [ ] 키보드 Tab만으로 모든 링크 · 버튼에 접근할 수 있고 포커스가 눈에 보인다.
- [ ] Lighthouse Performance / Accessibility / SEO 각 90점 이상.
- [ ] 카카오톡 · 링크드인에 링크를 공유했을 때 OG 카드가 정상 노출된다.

---

## 13. 향후 계획 (Future Scope)

| 버전 | 내용 |
|---|---|
| v1.1 | 이력서 PDF 다운로드, Skills 클릭 시 프로젝트 필터링 |
| v1.2 | 프로젝트 상세 페이지 분리 (아키텍처 다이어그램, 성능 비교 그래프 게재) |
| v2.0 | 영문 버전(ko/en 토글), 기술 블로그(Next.js + MDX) |
| v2.1 | RAG 챗봇 프로젝트를 사이트에 임베드하여 "나에 대해 물어보세요" 데모 제공 |

---

## 14. 열린 이슈 (Open Questions)

1. 원본 이력서의 GitHub 주소 · 이메일 · 전화번호가 예시 값(`example-hanyang-ai`, `lee.hanyang@example.com`, `010-0000-0000`)이다. **실제 정보로 교체가 필요하다.**
2. 각 프로젝트에서 본인이 담당한 파트와 정량 성과(분류 정확도 %, RAG 답변 정확도 개선 폭 등)를 추가할 수 있는가? 면접관 설득력에 가장 큰 영향을 준다.
3. 프로필 사진을 게재할 것인가? (Hero 레이아웃이 달라진다)
4. 전화번호를 공개할 것인가, 이메일만 노출할 것인가?
5. 커스텀 도메인을 사용할 것인가, `github.io` 기본 도메인을 사용할 것인가?
