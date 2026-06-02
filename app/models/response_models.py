from typing import List, Optional
from pydantic import BaseModel
from app.models.claim_models import ExtractedFields


class ClaimResponse(BaseModel):
    extractedFields: ExtractedFields
    missingFields: List[str]
    recommendedRoute: str
    reasoning: str


class HealthResponse(BaseModel):
    status: str
    version: str
    model: str


class ErrorResponse(BaseModel):
    detail: str
    error_type: Optional[str] = None
