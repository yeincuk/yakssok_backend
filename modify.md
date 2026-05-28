# 약쏙(Yakssok) 백엔드 리팩토링 및 수정 계획 (modify.md)

이 문서는 현재 약쏙 백엔드 프로젝트의 전체적인 문제점을 분석하고, 이를 수정하기 위한 구체적인 액션 플랜을 담고 있습니다.

## 1. 보안 상의 문제점 (Security Issues)

* **문제점 1: OpenAI API 키 하드코딩**
  * **원인**: `routers/ocr.py`, `routers/matching.py` 파일 내부에 `sk-proj-...` 형식의 API 키가 텍스트로 직접 노출되어 있습니다.
  * **해결 제안**:
    1. 노출된 기존 API 키를 즉시 폐기(Revoke)하고 새 키를 발급받습니다.
    2. `.env` 파일에 `OPENAI_API_KEY=새_키` 형태로 저장합니다.
    3. 소스 코드에서는 `os.getenv("OPENAI_API_KEY")`를 통해 로드하여 사용하도록 수정합니다.

* **문제점 2: 취약한 비밀번호 해싱 알고리즘**
  * **원인**: `auth.py`에서 `sha256_crypt` 방식을 사용 중입니다.
  * **해결 제안**: 이미 `requirements.txt`에 포함된 강력한 암호화 방식인 `bcrypt`로 교체합니다. (`CryptContext(schemes=["bcrypt"])`)

* **문제점 3: JWT Secret 노출 및 만료 처리 한계**
  * **원인**: `os.getenv`의 기본값으로 `"yakssok-secret"` 이라는 문자열이 하드코딩 되어 있습니다.
  * **해결 제안**: 실제 운영 환경에서는 `.env`에 `JWT_SECRET`이 없으면 서버 구동 자체를 막아버리도록 방어 로직을 추가합니다.

---

## 2. 코드 상의 문제점 (Code Issues)

* **문제점 1: Pydantic 모델과 라우터의 결합 (아키텍처 문제)**
  * **원인**: `models/` 디렉토리가 비어 있고, API 요청/응답 검증을 위한 `BaseModel` 상속 클래스들이 각 라우터 파일에 분산되어 섞여 있습니다.
  * **해결 제안**: `models/` 폴더 하위에 `user_schemas.py`, `medication_schemas.py`, `guardian_schemas.py` 등을 생성하여 스키마를 분리하고, 라우터에서는 이를 import 해서 쓰도록 리팩토링합니다.

* **문제점 2: 파이썬 표준 라이브러리 Deprecated(지원 중단) 함수 사용**
  * **원인**: 데이터 저장 시 `datetime.utcnow()`를 사용하고 있으며, Pydantic v2 환경에서 `dict()` 메서드를 사용 중입니다.
  * **해결 제안**: 
    1. `datetime.utcnow()` ➔ `datetime.now(timezone.utc)` 로 일괄 변경.
    2. `req.dict()` ➔ `req.model_dump()` 로 일괄 변경.

* **문제점 3: 하드코딩된 Colab 주소**
  * **원인**: `identify.py`에 Colab 임시 주소(`trycloudflare.com`)가 박혀 있어 주소가 바뀔 때마다 코드를 고쳐야 합니다.
  * **해결 제안**: `.env`에 `COLAB_IDENTIFY_URL`을 만들고 동적으로 읽어오게 수정합니다.

---

## 3. 예외처리 문제점 (Exception Handling Issues)

* **문제점 1: 광범위한 예외 무시(Swallow) 및 로깅 부재**
  * **원인**: `try-except Exception as e`로 모든 에러를 포착한 뒤, 서버 콘솔에 에러의 정확한 줄 번호(Stack Trace)를 출력하지 않고 500 에러를 반환합니다. 파이썬 `logging` 모듈도 사용되지 않았습니다.
  * **해결 제안**: 
    1. 파이썬 기본 내장 `logging` 모듈을 도입합니다. (`import logging; logger = logging.getLogger(__name__)`)
    2. 예외가 발생하면 `logger.exception("AI 분석 중 에러 발생")` 을 호출하여 백엔드 서버에 원인을 남깁니다.

* **문제점 2: 외부 API 및 JSON 파싱 실패에 대한 대비 부재**
  * **원인**: OpenAI가 JSON이 아닌 텍스트를 던지거나, Colab 서버가 응답하지 않을 때 시스템이 대처하지 못하고 죽습니다.
  * **해결 제안**: 
    1. `json.loads()` 부분에서 `json.JSONDecodeError`를 명시적으로 잡아서 "AI 응답 파싱 실패"라는 502(Bad Gateway) 에러를 냅니다.
    2. `httpx.post()` 부분에 타임아웃 예외 처리를 추가합니다.

---

## 4. 그외 문제점 (Other Issues)

* **문제점 1: 의존성 주입(Dependency Injection) 미활용**
  * **원인**: 각 엔드포인트마다 함수 내부에서 `db = get_db()`를 직접 호출하고 있습니다.
  * **해결 제안**: FastAPI의 강력한 기능인 의존성 주입을 활용하여, 파라미터단에서 `db: firestore.Client = Depends(get_db)` 형태로 주입받도록 수정하면 코드가 훨씬 깔끔해지고 테스트 코드 작성이 쉬워집니다.

* **문제점 2: CORS 설정 하드코딩**
  * **원인**: `main.py`에 허용할 도메인(localhost, ngrok 주소 등)이 고정되어 있습니다.
  * **해결 제안**: `.env`에서 `ALLOWED_ORIGINS="http://localhost:5173,https://..."` 형태로 받아와서 `main.py`에 주입하도록 변경합니다.
