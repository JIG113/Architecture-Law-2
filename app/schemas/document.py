from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    document_id: str
    filename: str
    status: str


class AnalyzeRequest(BaseModel):
    run_ocr: bool = True
    run_extraction: bool = True
    run_classification: bool = True


class AnalyzeResponse(BaseModel):
    document_id: str
    status: str
    confidence_score: float = Field(ge=0, le=1)


class SearchItem(BaseModel):
    document_id: str
    category_id: str
    field_name: str
    value: str
    source_page: int


class SearchResponse(BaseModel):
    query: str
    total: int
    items: list[SearchItem]


class EvidenceResponse(BaseModel):
    document_id: str
    field_name: str
    page_no: int
    snippet: str
    bbox: list[int]
