import pytest
from unittest.mock import AsyncMock, patch
from app.services.extraction_service import extract_claim_fields
from app.models.claim_models import ExtractedFields


MOCK_EXTRACTED = {
    "policyNumber": "POL-2024-789456",
    "policyholderName": "Jane Smith",
    "effectiveDates": "01/01/2024 - 12/31/2024",
    "incidentDate": "03/15/2024",
    "incidentTime": "14:30",
    "incidentLocation": "123 Main St, Springfield, IL",
    "incidentDescription": "Vehicle rear-ended at traffic light.",
    "claimantName": "Jane Smith",
    "thirdParties": ["John Doe"],
    "contactDetails": "jane.smith@email.com",
    "assetType": "Automobile",
    "assetId": "VIN: 1HGCM82633A123456",
    "estimatedDamage": "$8,500",
    "claimType": "auto",
    "attachments": ["police_report.pdf"],
    "initialEstimate": "$8,500",
}


@pytest.mark.asyncio
async def test_extract_valid_document():
    with patch(
        "app.services.extraction_service.extract_structured_output",
        new=AsyncMock(return_value=MOCK_EXTRACTED),
    ):
        result = await extract_claim_fields("Sample FNOL document text")
    assert isinstance(result, ExtractedFields)
    assert result.policyNumber == "POL-2024-789456"
    assert result.claimantName == "Jane Smith"


@pytest.mark.asyncio
async def test_extract_empty_document_returns_empty_fields():
    result = await extract_claim_fields("")
    assert isinstance(result, ExtractedFields)
    assert result.policyNumber is None


@pytest.mark.asyncio
async def test_extract_whitespace_only_returns_empty_fields():
    result = await extract_claim_fields("   \n\t  ")
    assert isinstance(result, ExtractedFields)
    assert result.claimantName is None


@pytest.mark.asyncio
async def test_extract_handles_api_exception():
    with patch(
        "app.services.extraction_service.extract_structured_output",
        new=AsyncMock(side_effect=Exception("API error")),
    ):
        result = await extract_claim_fields("Some document text")
    assert isinstance(result, ExtractedFields)
    assert result.policyNumber is None


@pytest.mark.asyncio
async def test_extract_returns_third_parties_as_list():
    with patch(
        "app.services.extraction_service.extract_structured_output",
        new=AsyncMock(return_value=MOCK_EXTRACTED),
    ):
        result = await extract_claim_fields("Sample text")
    assert isinstance(result.thirdParties, list)
    assert "John Doe" in result.thirdParties


@pytest.mark.asyncio
async def test_extract_partial_fields():
    partial = {**MOCK_EXTRACTED, "incidentTime": None, "assetId": None}
    with patch(
        "app.services.extraction_service.extract_structured_output",
        new=AsyncMock(return_value=partial),
    ):
        result = await extract_claim_fields("Partial document")
    assert result.incidentTime is None
    assert result.policyNumber == "POL-2024-789456"
