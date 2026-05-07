from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.schemas.document import (
    UploadResponse,
    AnalyzeRequest,
    AnalyzeResponse,
    SearchResponse,
    EvidenceResponse,
)
from app.services.pipeline import PipelineService

router = APIRouter()
service = PipelineService()


@router.post("/documents/upload", response_model=UploadResponse)
async def upload_document(
    source_type: str = Form(...),
    issuing_org: str = Form(...),
    file: UploadFile = File(...),
) -> UploadResponse:
    return await service.save_upload(source_type=source_type, issuing_org=issuing_org, file=file)


@router.post("/documents/{document_id}/analyze", response_model=AnalyzeResponse)
async def analyze_document(document_id: str, payload: AnalyzeRequest) -> AnalyzeResponse:
    result = service.analyze(document_id=document_id, payload=payload)
    if not result:
        raise HTTPException(status_code=404, detail="document not found")
    return result


@router.get("/search", response_model=SearchResponse)
def search(q: str, category: str | None = None, region: str | None = None) -> SearchResponse:
    return service.search(q=q, category=category, region=region)


@router.get("/documents/{document_id}/evidence", response_model=EvidenceResponse)
def get_evidence(document_id: str, field: str) -> EvidenceResponse:
    evidence = service.get_evidence(document_id=document_id, field=field)
    if not evidence:
        raise HTTPException(status_code=404, detail="evidence not found")
    return evidence
