import pytest
from app.models.claim_models import ExtractedFields
from app.services.validation_service import validate_claim


def test_all_mandatory_fields_present(sample_extracted_fields):
    missing = validate_claim(sample_extracted_fields)
    assert missing == []


def test_missing_policy_number():
    fields = ExtractedFields(
        policyNumber=None,
        claimType="auto",
        incidentDate="03/15/2024",
        estimatedDamage="$8,500",
        claimantName="Jane Smith",
    )
    missing = validate_claim(fields)
    assert "Policy Number" in missing


def test_missing_claim_type():
    fields = ExtractedFields(
        policyNumber="POL-123",
        claimType=None,
        incidentDate="03/15/2024",
        estimatedDamage="$8,500",
        claimantName="Jane Smith",
    )
    missing = validate_claim(fields)
    assert "Claim Type" in missing


def test_missing_incident_date():
    fields = ExtractedFields(
        policyNumber="POL-123",
        claimType="auto",
        incidentDate=None,
        estimatedDamage="$8,500",
        claimantName="Jane Smith",
    )
    missing = validate_claim(fields)
    assert "Incident Date" in missing


def test_missing_estimated_damage():
    fields = ExtractedFields(
        policyNumber="POL-123",
        claimType="auto",
        incidentDate="03/15/2024",
        estimatedDamage=None,
        claimantName="Jane Smith",
    )
    missing = validate_claim(fields)
    assert "Estimated Damage" in missing


def test_missing_claimant_name():
    fields = ExtractedFields(
        policyNumber="POL-123",
        claimType="auto",
        incidentDate="03/15/2024",
        estimatedDamage="$8,500",
        claimantName=None,
    )
    missing = validate_claim(fields)
    assert "Claimant Name" in missing


def test_all_mandatory_fields_missing():
    fields = ExtractedFields()
    missing = validate_claim(fields)
    assert len(missing) == 16
    assert "Policy Number" in missing
    assert "Policyholder Name" in missing
    assert "Effective Dates" in missing
    assert "Incident Date" in missing
    assert "Incident Time" in missing
    assert "Incident Location" in missing
    assert "Incident Description" in missing
    assert "Claimant Name" in missing
    assert "Third Parties" in missing
    assert "Contact Details" in missing
    assert "Asset Type" in missing
    assert "Asset ID" in missing
    assert "Estimated Damage" in missing
    assert "Claim Type" in missing
    assert "Attachments" in missing
    assert "Initial Estimate" in missing


def test_empty_string_treated_as_missing():
    fields = ExtractedFields(
        policyNumber="",
        claimType="auto",
        incidentDate="03/15/2024",
        estimatedDamage="$8,500",
        claimantName="Jane Smith",
    )
    missing = validate_claim(fields)
    assert "Policy Number" in missing


def test_whitespace_string_treated_as_missing():
    fields = ExtractedFields(
        policyNumber="   ",
        claimType="auto",
        incidentDate="03/15/2024",
        estimatedDamage="$8,500",
        claimantName="Jane Smith",
    )
    missing = validate_claim(fields)
    assert "Policy Number" in missing
