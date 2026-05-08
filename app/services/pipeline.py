from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from fastapi import UploadFile
from app.schemas.document import (
    UploadResponse,
    AnalyzeRequest,
    AnalyzeResponse,
    SearchResponse,
    SearchItem,
    EvidenceResponse,
)


@dataclass
class ExtractedField:
    category_id: str
    field_name: str
    value: str
    page_no: int
    snippet: str
    bbox: list[int] = field(default_factory=lambda: [100, 100, 300, 130])


@dataclass
class DocumentRecord:
    document_id: str
    filename: str
    source_type: str
    issuing_org: str
    analyzed: bool = False
    confidence_score: float = 0.0
    fields: dict[str, ExtractedField] = field(default_factory=dict)


class PipelineService:
    def __init__(self) -> None:
        self._docs: dict[str, DocumentRecord] = {}

    async def save_upload(self, source_type: str, issuing_org: str, file: UploadFile) -> UploadResponse:
        document_id = f"DOC-{uuid.uuid4().hex[:8].upper()}"
        self._docs[document_id] = DocumentRecord(
            document_id=document_id,
            filename=file.filename,
            source_type=source_type,
            issuing_org=issuing_org,
        )
        return UploadResponse(document_id=document_id, filename=file.filename, status="uploaded")

    def analyze(self, document_id: str, payload: AnalyzeRequest) -> AnalyzeResponse | None:
        doc = self._docs.get(document_id)
        if not doc:
            return None

        if payload.run_extraction:
            doc.fields = {
                "project_name": ExtractedField("C1-1", "project_name", "샘플 공공주택사업", 1, "사업명: 샘플 공공주택사업"),
                "site_area_m2": ExtractedField("C2-1", "site_area_m2", "35,722", 2, "부지면적 35,722㎡"),
                "submission_end": ExtractedField("C5-3", "submission_end", "2026-05-16T18:00:00+09:00", 4, "접수마감 2026.05.16 18:00"),
            }

        doc.analyzed = True
        doc.confidence_score = 0.91
        return AnalyzeResponse(document_id=document_id, status="analyzed", confidence_score=doc.confidence_score)

    def search(self, q: str, category: str | None = None, region: str | None = None) -> SearchResponse:
        items: list[SearchItem] = []
        for doc in self._docs.values():
            for field_data in doc.fields.values():
                if q in field_data.value or q in field_data.snippet or q in field_data.field_name:
                    if category and field_data.category_id != category:
                        continue
                    items.append(
                        SearchItem(
                            document_id=doc.document_id,
                            category_id=field_data.category_id,
                            field_name=field_data.field_name,
                            value=field_data.value,
                            source_page=field_data.page_no,
                        )
                    )
        return SearchResponse(query=q, total=len(items), items=items)

    def get_evidence(self, document_id: str, field: str) -> EvidenceResponse | None:
        doc = self._docs.get(document_id)
        if not doc or field not in doc.fields:
            return None
        info = doc.fields[field]
        return EvidenceResponse(
            document_id=document_id,
            field_name=field,
            page_no=info.page_no,
            snippet=info.snippet,
            bbox=info.bbox,
        )
