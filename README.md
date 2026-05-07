# Architecture-Law-2

건축 사업 공고/고시/지침 문서를 업로드하고, 자동 분석/분류/검색/근거 열람을 수행하는 MVP API 템플릿입니다.

## 폴더 구조

- `app/main.py`: FastAPI 진입점
- `app/api/routes.py`: 업로드/분석/검색/근거 API
- `app/services/pipeline.py`: 인메모리 파이프라인 서비스 샘플
- `app/schemas/document.py`: 요청/응답 스키마
- `app/core/category_template.json`: 카테고리 템플릿
- `scripts/sample_curl.sh`: 업로드 예시 호출

## 실행

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API

### 1) 문서 업로드
`POST /api/documents/upload`

Form-data:
- `source_type`: 공고/고시/지침
- `issuing_org`: 발행기관
- `file`: 파일

### 2) 분석 실행
`POST /api/documents/{document_id}/analyze`

```json
{
  "run_ocr": true,
  "run_extraction": true,
  "run_classification": true
}
```

### 3) 검색
`GET /api/search?q=35,722&category=C2-1`

### 4) 근거 열람
`GET /api/documents/{document_id}/evidence?field=site_area_m2`

## 다음 단계(권장)

- OCR 엔진 및 PDF 파서 연결
- DB(PostgreSQL) 및 검색 인덱스(OpenSearch) 연동
- 벡터 검색(RAG) 추가
- 검수 UI/권한관리/로그 고도화
