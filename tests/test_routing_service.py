import pytest
from app.models.claim_models import ExtractedFields
from app.services.routing_service import determine_route


def test_fast_track_route(sample_extracted_fields):
    # $8,500 < $25,000 with no missing fields
    route = determine_route(sample_extracted_fields, [])
    assert route == "Fast-track"


def test_manual_review_route(missing_fields_extracted):
    route = determine_route(missing_fields_extracted, ["Policy Number", "Claim Type"])
    assert route == "Manual Review"


def test_investigation_flag_route(fraud_extracted_fields):
    route = determine_route(fraud_extracted_fields, [])
    assert route == "Investigation Flag"


def test_specialist_queue_route(injury_extracted_fields):
    route = determine_route(injury_extracted_fields, [])
    assert route == "Specialist Queue"


def test_standard_processing_route(high_damage_extracted_fields):
    route = determine_route(high_damage_extracted_fields, [])
    assert route == "Standard Processing"


def test_investigation_flag_beats_manual_review(fraud_extracted_fields):
    # Even with missing fields, fraud takes priority
    route = determine_route(fraud_extracted_fields, ["Policy Number"])
    assert route == "Investigation Flag"


def test_investigation_flag_beats_specialist_queue():
    fields = ExtractedFields(
        policyNumber="POL-123",
        claimType="injury",
        incidentDate="03/15/2024",
        estimatedDamage="$8,000",
        claimantName="Jane Smith",
        incidentDescription="This accident was clearly staged for insurance fraud.",
    )
    route = determine_route(fields, [])
    assert route == "Investigation Flag"


def test_manual_review_beats_specialist_queue():
    fields = ExtractedFields(
        claimType="injury",
        incidentDate="03/15/2024",
        estimatedDamage="$8,000",
        claimantName="Jane Smith",
    )
    route = determine_route(fields, ["Policy Number"])
    assert route == "Manual Review"


def test_case_insensitive_fraud_keyword():
    fields = ExtractedFields(
        policyNumber="POL-123",
        claimType="auto",
        incidentDate="03/15/2024",
        estimatedDamage="$8,000",
        claimantName="Jane Smith",
        incidentDescription="Evidence suggests FRAUD in this claim.",
    )
    route = determine_route(fields, [])
    assert route == "Investigation Flag"


def test_inconsistent_keyword_triggers_investigation():
    fields = ExtractedFields(
        policyNumber="POL-123",
        claimType="auto",
        incidentDate="03/15/2024",
        estimatedDamage="$8,000",
        claimantName="Jane Smith",
        incidentDescription="The stories from both parties are inconsistent.",
    )
    route = determine_route(fields, [])
    assert route == "Investigation Flag"


def test_exact_threshold_not_fast_track():
    fields = ExtractedFields(
        policyNumber="POL-123",
        claimType="auto",
        incidentDate="03/15/2024",
        estimatedDamage="$25,000",
        claimantName="Jane Smith",
    )
    route = determine_route(fields, [])
    assert route == "Standard Processing"


def test_no_damage_value_goes_to_standard():
    fields = ExtractedFields(
        policyNumber="POL-123",
        claimType="auto",
        incidentDate="03/15/2024",
        estimatedDamage=None,
        claimantName="Jane Smith",
    )
    # estimatedDamage is None — cannot be parsed, so not fast-track
    route = determine_route(fields, [])
    assert route == "Standard Processing"
