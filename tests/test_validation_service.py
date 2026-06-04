import pytest
from app.models.claim_models import ExtractedFields
from app.services.validation_service import validate_claim, MANDATORY_FIELDS

ALL_MANDATORY_DISPLAY_NAMES = [display for _, display in MANDATORY_FIELDS]


# ---------------------------------------------------------------------------
# Full coverage — all 16 fields present
# ---------------------------------------------------------------------------
def test_no_missing_fields_when_all_present(sample_extracted_fields):
    result = validate_claim(sample_extracted_fields)
    assert result == [], f"Expected no missing fields, got: {result}"


def test_mandatory_fields_list_has_16_entries():
    assert len(MANDATORY_FIELDS) == 16, (
        f"Assignment requires 16 mandatory fields, found {len(MANDATORY_FIELDS)}"
    )


# ---------------------------------------------------------------------------
# Each mandatory field individually
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("field_key,display_name", MANDATORY_FIELDS)
def test_each_mandatory_field_flagged_when_none(field_key, display_name, sample_extracted_fields):
    setattr(sample_extracted_fields, field_key, None)
    missing = validate_claim(sample_extracted_fields)
    assert display_name in missing, f"Expected '{display_name}' in missing, got: {missing}"


@pytest.mark.parametrize("field_key,display_name", [
    ("policyNumber",     "Policy Number"),
    ("policyholderName", "Policyholder Name"),
    ("claimantName",     "Claimant Name"),
    ("incidentLocation", "Incident Location"),
])
def test_whitespace_only_string_treated_as_missing(field_key, display_name, sample_extracted_fields):
    setattr(sample_extracted_fields, field_key, "   ")
    missing = validate_claim(sample_extracted_fields)
    assert display_name in missing


@pytest.mark.parametrize("field_key,display_name", [
    ("policyNumber",  "Policy Number"),
    ("claimantName",  "Claimant Name"),
    ("estimatedDamage", "Estimated Damage"),
])
def test_empty_string_treated_as_missing(field_key, display_name, sample_extracted_fields):
    setattr(sample_extracted_fields, field_key, "")
    missing = validate_claim(sample_extracted_fields)
    assert display_name in missing


# ---------------------------------------------------------------------------
# List fields
# ---------------------------------------------------------------------------
def test_empty_third_parties_list_flagged(sample_extracted_fields):
    sample_extracted_fields.thirdParties = []
    missing = validate_claim(sample_extracted_fields)
    assert "Third Parties" in missing


def test_empty_attachments_list_flagged(sample_extracted_fields):
    sample_extracted_fields.attachments = []
    missing = validate_claim(sample_extracted_fields)
    assert "Attachments" in missing


def test_populated_list_fields_not_flagged(sample_extracted_fields):
    sample_extracted_fields.thirdParties = ["Austin Fire Department"]
    sample_extracted_fields.attachments = ["fire_report.pdf"]
    missing = validate_claim(sample_extracted_fields)
    assert "Third Parties" not in missing
    assert "Attachments" not in missing


# ---------------------------------------------------------------------------
# All fields missing
# ---------------------------------------------------------------------------
def test_all_fields_missing_returns_16(incomplete_claim_fields):
    blank = ExtractedFields()
    missing = validate_claim(blank)
    assert len(missing) == 16
    for display_name in ALL_MANDATORY_DISPLAY_NAMES:
        assert display_name in missing


# ---------------------------------------------------------------------------
# Partial missing
# ---------------------------------------------------------------------------
def test_partial_missing_returns_correct_count(sample_extracted_fields):
    sample_extracted_fields.effectiveDates = None
    sample_extracted_fields.incidentTime = None
    sample_extracted_fields.assetId = None
    missing = validate_claim(sample_extracted_fields)
    assert len(missing) == 3
    assert "Effective Dates" in missing
    assert "Incident Time" in missing
    assert "Asset ID" in missing


def test_missing_fields_returns_display_names_not_keys():
    """Returned names must be human-readable, not camelCase keys."""
    fields = ExtractedFields(policyNumber=None, claimantName=None)
    missing = validate_claim(fields)
    assert "policyNumber" not in missing
    assert "claimantName" not in missing
    assert "Policy Number" in missing
    assert "Claimant Name" in missing
