import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.fixture
def sample_extracted_fields():
    from app.models.claim_models import ExtractedFields
    return ExtractedFields(
        policyNumber="POL-2024-789456",
        policyholderName="Jane Smith",
        effectiveDates="01/01/2024 - 12/31/2024",
        incidentDate="03/15/2024",
        incidentTime="14:30",
        incidentLocation="123 Main St, Springfield, IL",
        incidentDescription="Vehicle rear-ended at traffic light causing bumper damage.",
        claimantName="Jane Smith",
        thirdParties=["John Doe"],
        contactDetails="jane.smith@email.com | (555) 123-4567",
        assetType="Automobile",
        assetId="VIN: 1HGCM82633A123456",
        estimatedDamage="$8,500",
        claimType="auto",
        attachments=["police_report.pdf", "photos.zip"],
        initialEstimate="$8,500",
    )


@pytest.fixture
def missing_fields_extracted():
    from app.models.claim_models import ExtractedFields
    return ExtractedFields(
        policyNumber=None,
        claimType=None,
        incidentDate="03/15/2024",
        estimatedDamage="$8,500",
        claimantName="Jane Smith",
    )


@pytest.fixture
def fraud_extracted_fields(sample_extracted_fields):
    sample_extracted_fields.incidentDescription = (
        "The accident appears to be staged and shows signs of fraud."
    )
    return sample_extracted_fields


@pytest.fixture
def injury_extracted_fields(sample_extracted_fields):
    sample_extracted_fields.claimType = "injury"
    sample_extracted_fields.estimatedDamage = "$30,000"
    return sample_extracted_fields


@pytest.fixture
def high_damage_extracted_fields(sample_extracted_fields):
    sample_extracted_fields.estimatedDamage = "$75,000"
    return sample_extracted_fields


@pytest.fixture
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
