import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.models.claim_models import ExtractedFields


# ---------------------------------------------------------------------------
# Base fixture — property fire claim, all 16 fields populated
# ---------------------------------------------------------------------------
@pytest.fixture
def sample_extracted_fields():
    return ExtractedFields(
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


@pytest.fixture
def incomplete_claim_fields():
    """Fixture with most optional fields absent — triggers Manual Review."""
    return ExtractedFields(
        incidentDate="11/03/2025",
        claimantName="Marcus Webb",
    )


@pytest.fixture
def fraud_extracted_fields(sample_extracted_fields):
    sample_extracted_fields.incidentDescription = (
        "Witness accounts are inconsistent with physical evidence, suggesting a staged incident."
    )
    return sample_extracted_fields


@pytest.fixture
def injury_claim_fields(sample_extracted_fields):
    sample_extracted_fields.claimType = "injury"
    sample_extracted_fields.estimatedDamage = "$41,000"
    return sample_extracted_fields


@pytest.fixture
def high_value_claim_fields(sample_extracted_fields):
    sample_extracted_fields.estimatedDamage = "$62,500"
    return sample_extracted_fields


@pytest.fixture
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        yield client
