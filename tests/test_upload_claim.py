import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.models.claim_models import ExtractedFields

MOCK_EXTRACTED_FIELDS = ExtractedFields(
    policyNumber="POL-2024-789456",
    policyholderName="Jane Smith",
    effectiveDates="01/01/2024 - 12/31/2024",
    incidentDate="03/15/2024",
    incidentTime="14:30",
    incidentLocation="123 Main St, Springfield, IL",
    incidentDescription="Vehicle rear-ended at traffic light.",
    claimantName="Jane Smith",
    thirdParties=["John Doe"],
    contactDetails="jane.smith@email.com",
    assetType="Automobile",
    assetId="VIN: 1HGCM82633A123456",
    estimatedDamage="$8,500",
    claimType="auto",
    attachments=["police_report.pdf"],
    initialEstimate="$8,500",
)

SAMPLE_TXT = b"""FNOL REPORT
Policy Number: POL-2024-789456
Policyholder: Jane Smith
Claimant: Jane Smith
Incident Date: 03/15/2024
Incident Time: 14:30
Location: 123 Main St, Springfield, IL
Description: Vehicle rear-ended at traffic light.
Claim Type: auto
Estimated Damage: $8,500
"""


@pytest.mark.asyncio
async def test_upload_txt_claim_success():
    with patch(
        "app.routers.claim_router.extract_claim_fields",
        new=AsyncMock(return_value=MOCK_EXTRACTED_FIELDS),
    ):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/upload-claim",
                files={"file": ("test_claim.txt", SAMPLE_TXT, "text/plain")},
            )

    assert response.status_code == 200
    data = response.json()
    assert "extractedFields" in data
    assert "missingFields" in data
    assert "recommendedRoute" in data
    assert "reasoning" in data


@pytest.mark.asyncio
async def test_upload_invalid_file_type():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/upload-claim",
            files={"file": ("test.docx", b"some content", "application/vnd.openxmlformats")},
        )
    assert response.status_code == 415


@pytest.mark.asyncio
async def test_upload_empty_file():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/upload-claim",
            files={"file": ("empty.txt", b"", "text/plain")},
        )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_upload_no_file():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post("/upload-claim")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_response_contains_recommended_route():
    with patch(
        "app.routers.claim_router.extract_claim_fields",
        new=AsyncMock(return_value=MOCK_EXTRACTED_FIELDS),
    ):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/upload-claim",
                files={"file": ("claim.txt", SAMPLE_TXT, "text/plain")},
            )
    data = response.json()
    assert data["recommendedRoute"] in [
        "Fast-track",
        "Manual Review",
        "Investigation Flag",
        "Specialist Queue",
        "Standard Processing",
    ]


@pytest.mark.asyncio
async def test_upload_txt_with_missing_fields():
    incomplete = ExtractedFields(incidentDate="03/15/2024", claimantName="Jane Smith")
    with patch(
        "app.routers.claim_router.extract_claim_fields",
        new=AsyncMock(return_value=incomplete),
    ):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/upload-claim",
                files={"file": ("claim.txt", SAMPLE_TXT, "text/plain")},
            )
    data = response.json()
    assert response.status_code == 200
    assert len(data["missingFields"]) > 0
    assert data["recommendedRoute"] == "Manual Review"
