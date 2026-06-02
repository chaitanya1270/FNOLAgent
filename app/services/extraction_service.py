import json
from typing import Dict, Any

from pydantic import BaseModel
from typing import List, Optional

from app.models.claim_models import ExtractedFields
from app.prompts.extraction_prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from app.services.azure_openai_client import extract_structured_output
from app.utils.logger import get_logger

logger = get_logger(__name__)


class AIExtractedFields(BaseModel):
    """Schema enforced by Azure OpenAI structured outputs."""
    policyNumber: Optional[str] = None
    policyholderName: Optional[str] = None
    effectiveDates: Optional[str] = None
    incidentDate: Optional[str] = None
    incidentTime: Optional[str] = None
    incidentLocation: Optional[str] = None
    incidentDescription: Optional[str] = None
    claimantName: Optional[str] = None
    thirdParties: List[str] = []
    contactDetails: Optional[str] = None
    assetType: Optional[str] = None
    assetId: Optional[str] = None
    estimatedDamage: Optional[str] = None
    claimType: Optional[str] = None
    attachments: List[str] = []
    initialEstimate: Optional[str] = None


async def extract_claim_fields(document_text: str) -> ExtractedFields:
    """Use Azure OpenAI structured outputs to extract claim fields from document text."""
    if not document_text.strip():
        logger.warning("Empty document text passed to extraction service")
        return ExtractedFields()

    user_prompt = USER_PROMPT_TEMPLATE.format(document_text=document_text)

    try:
        raw: Dict[str, Any] = await extract_structured_output(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_schema=AIExtractedFields,
        )
        logger.info("Extraction successful")
        return ExtractedFields(**raw)
    except json.JSONDecodeError as exc:
        logger.error("JSON decode error during extraction: %s", exc)
        return ExtractedFields()
    except Exception as exc:
        logger.error("Extraction failed: %s", exc)
        return ExtractedFields()
