# Architecture-Law-2

건축 사업 공고/고시/지침 문서를 업로드하고, 자동 분석/분류/검색/근거 열람을 수행하는 MVP API 템플릿입니다.

## 1) 서버로 실행(개발용)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

- API 문서: `http://127.0.0.1:8000/docs`
- 헬스체크: `http://127.0.0.1:8000/health`

## 2) 실행형 프로그램(데스크톱 런처)

서버 명령어를 모르는 사용자를 위해 `desktop_app.py`를 추가했습니다.
런처에서 버튼으로 서버를 시작/중지하고 Swagger 페이지를 바로 열 수 있습니다.

### 런처 직접 실행
```bash
python desktop_app.py
```

### EXE 빌드 (PyInstaller)
```bash
./build_desktop.sh
```

빌드 완료 후:
- macOS/Linux: `dist/ArchitectureNoticeLauncher`
- Windows(동일 명령 실행 시): `dist/ArchitectureNoticeLauncher.exe`

## API 요약

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
