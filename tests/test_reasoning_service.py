import pytest
from app.models.claim_models import ExtractedFields
from app.services.reasoning_service import generate_reasoning


def test_reasoning_for_fast_track(sample_extracted_fields):
    reasoning = generate_reasoning("Fast-track", sample_extracted_fields, [])
    assert "Fast-track" in reasoning
    assert "$" in reasoning
    assert "25,000" in reasoning


def test_reasoning_for_manual_review(sample_extracted_fields):
    missing = ["Policy Number", "Claim Type"]
    reasoning = generate_reasoning("Manual Review", sample_extracted_fields, missing)
    assert "Manual Review" in reasoning
    assert "Policy Number" in reasoning
    assert "Claim Type" in reasoning


def test_reasoning_for_investigation_flag(fraud_extracted_fields):
    reasoning = generate_reasoning("Investigation Flag", fraud_extracted_fields, [])
    assert "Investigation Flag" in reasoning
    assert any(kw in reasoning for kw in ["fraud", "staged", "inconsistent"])


def test_reasoning_for_specialist_queue(injury_extracted_fields):
    reasoning = generate_reasoning("Specialist Queue", injury_extracted_fields, [])
    assert "Specialist Queue" in reasoning
    assert "injury" in reasoning.lower()


def test_reasoning_for_standard_processing(high_damage_extracted_fields):
    reasoning = generate_reasoning("Standard Processing", high_damage_extracted_fields, [])
    assert "Standard Processing" in reasoning


def test_reasoning_is_non_empty_for_all_routes(sample_extracted_fields):
    routes = [
        "Fast-track",
        "Manual Review",
        "Investigation Flag",
        "Specialist Queue",
        "Standard Processing",
    ]
    for route in routes:
        reasoning = generate_reasoning(route, sample_extracted_fields, ["Policy Number"])
        assert isinstance(reasoning, str)
        assert len(reasoning) > 10
