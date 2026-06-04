import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.models.claim_models import ExtractedFields

# ---------------------------------------------------------------------------
# Shared mock data — property fire claim (Marcus Webb)
# ---------------------------------------------------------------------------
FULL_CLAIM = ExtractedFields(
    policyNumber="POL-2025-334872",
    policyholderName="Marcus Webb",
    effectiveDates="06/01/2025 - 05/31/2026",
    incidentDate="11/03/2025",
    incidentTime="09:45",
    incidentLocation="45 Riverside Drive, Austin, TX 78701",
    incidentDescription="Kitchen fire started from an electrical fault and spread to the living area.",
    claimantName="Marcus Webb",
    thirdParties=["Austin Fire Department"],
    contactDetails="marcus.webb@outlook.com | (512) 884-3301",
    assetType="Residential Property",
    assetId="APNs: 0247-TX-9981",
    estimatedDamage="$18,200",
    claimType="property",
    attachments=["fire_report.pdf", "damage_assessment.jpg"],
    initialEstimate="$18,200",
)

SAMPLE_FNOL_TXT = b"""FIRST NOTICE OF LOSS
Policy Number: POL-2025-334872
Policyholder: Marcus Webb
Effective Dates: 06/01/2025 - 05/31/2026
Incident Date: 11/03/2025
Incident Time: 09:45
Location: 45 Riverside Drive, Austin, TX 78701
Description: Kitchen fire from electrical fault.
Claimant: Marcus Webb
Contact: marcus.webb@outlook.com | (512) 884-3301
Third Parties: Austin Fire Department
Asset Type: Residential Property
Asset ID: APNs: 0247-TX-9981
Estimated Damage: $18,200
Claim Type: property
Attachments: fire_report.pdf
Initial Estimate: $18,200
"""

PATCH_TARGET = "app.routers.claim_router.extract_claim_fields"


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
def _post_txt(client, content=SAMPLE_FNOL_TXT, filename="claim.txt"):
    return client.post(
        "/upload-claim",
        files={"file": (filename, content, "text/plain")},
    )


# ---------------------------------------------------------------------------
# Success cases
# ---------------------------------------------------------------------------
class TestUploadSuccess:
    @pytest.mark.asyncio
    async def test_returns_200_for_valid_txt(self):
        with patch(PATCH_TARGET, new=AsyncMock(return_value=FULL_CLAIM)):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
                resp = await _post_txt(client)
        assert resp.status_code == 200

    @pytest.mark.asyncio
    async def test_response_contains_all_required_keys(self):
        with patch(PATCH_TARGET, new=AsyncMock(return_value=FULL_CLAIM)):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
                resp = await _post_txt(client)
        body = resp.json()
        for key in ("extractedFields", "missingFields", "recommendedRoute", "reasoning"):
            assert key in body, f"Missing key: {key}"

    @pytest.mark.asyncio
    async def test_recommended_route_is_valid_value(self):
        valid_routes = {"Fast-track", "Manual Review", "Investigation Flag", "Specialist Queue", "Standard Processing"}
        with patch(PATCH_TARGET, new=AsyncMock(return_value=FULL_CLAIM)):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
                resp = await _post_txt(client)
        assert resp.json()["recommendedRoute"] in valid_routes

    @pytest.mark.asyncio
    async def test_reasoning_is_non_empty_string(self):
        with patch(PATCH_TARGET, new=AsyncMock(return_value=FULL_CLAIM)):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
                resp = await _post_txt(client)
        reasoning = resp.json()["reasoning"]
        assert isinstance(reasoning, str) and len(reasoning) > 0

    @pytest.mark.asyncio
    async def test_full_claim_routes_to_fast_track(self):
        """All 16 fields present, $18,200 damage → Fast-track."""
        with patch(PATCH_TARGET, new=AsyncMock(return_value=FULL_CLAIM)):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
                resp = await _post_txt(client)
        assert resp.json()["recommendedRoute"] == "Fast-track"
        assert resp.json()["missingFields"] == []


# ---------------------------------------------------------------------------
# Missing field cases
# ---------------------------------------------------------------------------
class TestUploadMissingFields:
    @pytest.mark.asyncio
    async def test_incomplete_claim_triggers_manual_review(self):
        sparse = ExtractedFields(incidentDate="11/03/2025", claimantName="Marcus Webb")
        with patch(PATCH_TARGET, new=AsyncMock(return_value=sparse)):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
                resp = await _post_txt(client)
        body = resp.json()
        assert resp.status_code == 200
        assert body["recommendedRoute"] == "Manual Review"
        assert len(body["missingFields"]) > 0

    @pytest.mark.asyncio
    async def test_missing_fields_list_is_array(self):
        with patch(PATCH_TARGET, new=AsyncMock(return_value=FULL_CLAIM)):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
                resp = await _post_txt(client)
        assert isinstance(resp.json()["missingFields"], list)


# ---------------------------------------------------------------------------
# Validation / error cases
# ---------------------------------------------------------------------------
class TestUploadValidation:
    @pytest.mark.asyncio
    async def test_rejects_docx_with_415(self):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
            resp = await client.post(
                "/upload-claim",
                files={"file": ("report.docx", b"binary content", "application/vnd.openxmlformats")},
            )
        assert resp.status_code == 415

    @pytest.mark.asyncio
    async def test_rejects_empty_file_with_400(self):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
            resp = await client.post(
                "/upload-claim",
                files={"file": ("empty.txt", b"", "text/plain")},
            )
        assert resp.status_code == 400

    @pytest.mark.asyncio
    async def test_rejects_missing_file_field_with_422(self):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
            resp = await client.post("/upload-claim")
        assert resp.status_code == 422

    @pytest.mark.asyncio
    async def test_rejects_csv_file_type(self):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
            resp = await client.post(
                "/upload-claim",
                files={"file": ("data.csv", b"col1,col2\n1,2", "text/csv")},
            )
        assert resp.status_code == 415
