## 약쏙 백엔드
## 저시력자를 위한 복약 안전 서비스 '약쏙'의 백엔드 API 서버입니다.
처방전을 촬영하면 OCR로 약 정보를 등록하고, 복용 시점에 약을 촬영해
처방과 일치하는지 판단하며, 그 결과를 보호자가 함께 확인할 수 있습니다.

프론트엔드 레포: https://github.com/yeincuk/yakssok_frontend
데모: https://yakssok-frontend.vercel.app

# 기술 스택

Framework: FastAPI (Python)
Database / Infra: Firebase (Firestore, Auth)
AI: OpenAI API, 자체 AI 모델 서버 연동
배포: <!-- 배포한 플랫폼 (예: Railway, Render) -->

# 주요 API
라우터설명auth사용자 인증 / 회원가입ocr처방전 촬영 후 OCR로 약 정보 추출medication복약 정보 등록 및 관리matching촬영한 약이 처방과 일치하는지 판단 (match / check / fail)identify알약 식별guardian보호자 연동 (복약 현황 공유 및 조치)
프론트엔드의 복약 결과 상태(match / check / fail)와 동일한 체계로 연동됩니다.

# 아키텍처
요청을 Router → Service → Repository 3계층으로 분리헀습니다.

Router: API 엔드포인트, 요청/응답 처리
Service: 비즈니스 로직, 검증
Repository: 데이터 접근 (Firebase)
Model: 데이터 스키마

# 프로젝트 구조
yakssok_backend/
├── main.py               # FastAPI 진입점
├── firebase_config.py    # Firebase 초기화
├── requirements.txt
├── Procfile              # 배포 설정
├── routers/              # API 엔드포인트
├── services/             # 비즈니스 로직
├── repositories/         # 데이터 접근 계층
└── models/               # 데이터 스키마

# 실행 방법
bashpython -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env            # .env 값을 실제 값으로 채워주세요
uvicorn main:app --reload
환경 변수
.env.example을 참고해 .env를 작성합니다.
envOPENAI_API_KEY=your_openai_api_key_here


# Firebase, AI 모델 서버 주소 등 필요한 변수 추가
실제 .env와 firebase-key.json은 커밋하지 않습니다 (.gitignore 처리).
팀 구성 및 역할
역할담당AI 모델 개발팀원데이터셋 수집 및 논문 조사본인AI 모델 서버 연동본인백엔드 개발 (FastAPI)본인프론트엔드 개발 (React)본인UI/UX 디자인본인
관련 레포

프론트엔드: https://github.com/yeincuk/yakssok_frontend
AI 모델 서버: <!-- 팀원 레포 주소 (본인이 백엔드와 연동) -->
