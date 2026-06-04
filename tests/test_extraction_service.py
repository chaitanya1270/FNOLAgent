import pytest
from unittest.mock import AsyncMock, patch

from app.services.extraction_service import extract_claim_fields
from app.models.claim_models import ExtractedFields

PATCH_TARGET = "app.services.extraction_service.extract_structured_output"

MOCK_PROPERTY_CLAIM = {
    "policyNumber":       "POL-2025-334872",
    "policyholderName":   "Marcus Webb",
    "effectiveDates":     "06/01/2025 - 05/31/2026",
    "incidentDate":       "11/03/2025",
    "incidentTime":       "09:45",
    "incidentLocation":   "45 Riverside Drive, Austin, TX 78701",
    "incidentDescription":"Kitchen fire from electrical fault.",
    "claimantName":       "Marcus Webb",
    "thirdParties":       ["Austin Fire Department"],
    "contactDetails":     "marcus.webb@outlook.com | (512) 884-3301",
    "assetType":          "Residential Property",
    "assetId":            "APNs: 0247-TX-9981",
    "estimatedDamage":    "$18,200",
    "claimType":          "property",
    "attachments":        ["fire_report.pdf", "damage_assessment.jpg"],
    "initialEstimate":    "$18,200",
}


# ---------------------------------------------------------------------------
# Return type
# ---------------------------------------------------------------------------
class TestExtractionReturnType:
    @pytest.mark.asyncio
    async def test_returns_extracted_fields_instance(self):
        with patch(PATCH_TARGET, new=AsyncMock(return_value=MOCK_PROPERTY_CLAIM)):
            result = await extract_claim_fields("FNOL document text here")
        assert isinstance(result, ExtractedFields)

    @pytest.mark.asyncio
    async def test_empty_input_returns_extracted_fields_instance(self):
        result = await extract_claim_fields("")
        assert isinstance(result, ExtractedFields)

    @pytest.mark.asyncio
    async def test_whitespace_input_returns_extracted_fields_instance(self):
        result = await extract_claim_fields("\n\t  ")
        assert isinstance(result, ExtractedFields)


# ---------------------------------------------------------------------------
# Field mapping
# ---------------------------------------------------------------------------
class TestFieldMapping:
    @pytest.mark.asyncio
    async def test_policy_number_mapped_correctly(self):
        with patch(PATCH_TARGET, new=AsyncMock(return_value=MOCK_PROPERTY_CLAIM)):
            result = await extract_claim_fields("some text")
        assert result.policyNumber == "POL-2025-334872"

    @pytest.mark.asyncio
    async def test_claimant_name_mapped_correctly(self):
        with patch(PATCH_TARGET, new=AsyncMock(return_value=MOCK_PROPERTY_CLAIM)):
            result = await extract_claim_fields("some text")
        assert result.claimantName == "Marcus Webb"

    @pytest.mark.asyncio
    async def test_estimated_damage_mapped_correctly(self):
        with patch(PATCH_TARGET, new=AsyncMock(return_value=MOCK_PROPERTY_CLAIM)):
            result = await extract_claim_fields("some text")
        assert result.estimatedDamage == "$18,200"

    @pytest.mark.asyncio
    async def test_third_parties_is_list(self):
        with patch(PATCH_TARGET, new=AsyncMock(return_value=MOCK_PROPERTY_CLAIM)):
            result = await extract_claim_fields("some text")
        assert isinstance(result.thirdParties, list)
        assert "Austin Fire Department" in result.thirdParties

    @pytest.mark.asyncio
    async def test_attachments_is_list(self):
        with patch(PATCH_TARGET, new=AsyncMock(return_value=MOCK_PROPERTY_CLAIM)):
            result = await extract_claim_fields("some text")
        assert isinstance(result.attachments, list)
        assert len(result.attachments) == 2


# ---------------------------------------------------------------------------
# Null / guard behaviour
# ---------------------------------------------------------------------------
class TestExtractionGuards:
    @pytest.mark.asyncio
    async def test_empty_document_returns_none_fields(self):
        result = await extract_claim_fields("")
        assert result.policyNumber is None
        assert result.claimantName is None

    @pytest.mark.asyncio
    async def test_api_exception_returns_empty_fields(self):
        with patch(PATCH_TARGET, new=AsyncMock(side_effect=Exception("Service unavailable"))):
            result = await extract_claim_fields("Some claim document")
        assert isinstance(result, ExtractedFields)
        assert result.policyNumber is None

    @pytest.mark.asyncio
    async def test_partial_response_populates_available_fields(self):
        partial = {**MOCK_PROPERTY_CLAIM, "incidentTime": None, "assetId": None, "thirdParties": []}
        with patch(PATCH_TARGET, new=AsyncMock(return_value=partial)):
            result = await extract_claim_fields("Partial document")
        assert result.incidentTime is None
        assert result.assetId is None
        assert result.policyNumber == "POL-2025-334872"
