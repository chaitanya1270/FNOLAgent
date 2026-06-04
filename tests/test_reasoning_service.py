import pytest
from app.models.claim_models import ExtractedFields
from app.services.reasoning_service import generate_reasoning
from app.services.routing_service import ROUTES

ALL_ROUTES = list(ROUTES.values())


# ---------------------------------------------------------------------------
# Output contract
# ---------------------------------------------------------------------------
class TestReasoningContract:
    @pytest.mark.parametrize("route", ALL_ROUTES)
    def test_reasoning_always_returns_string(self, route, sample_extracted_fields):
        result = generate_reasoning(route, sample_extracted_fields, [])
        assert isinstance(result, str)

    @pytest.mark.parametrize("route", ALL_ROUTES)
    def test_reasoning_is_never_empty(self, route, sample_extracted_fields):
        result = generate_reasoning(route, sample_extracted_fields, ["Policy Number"])
        assert len(result.strip()) > 20, f"Reasoning too short for route '{route}'"

    def test_reasoning_contains_route_name_for_fast_track(self, sample_extracted_fields):
        result = generate_reasoning("Fast-track", sample_extracted_fields, [])
        assert "Fast-track" in result

    def test_reasoning_contains_route_name_for_standard(self, high_value_claim_fields):
        result = generate_reasoning("Standard Processing", high_value_claim_fields, [])
        assert "Standard Processing" in result


# ---------------------------------------------------------------------------
# Route-specific content checks
# ---------------------------------------------------------------------------
class TestReasoningContent:
    def test_fast_track_mentions_damage_amount(self, sample_extracted_fields):
        result = generate_reasoning("Fast-track", sample_extracted_fields, [])
        assert "$" in result
        assert "25,000" in result

    def test_fast_track_mentions_threshold(self, sample_extracted_fields):
        result = generate_reasoning("Fast-track", sample_extracted_fields, [])
        assert "25,000" in result

    def test_manual_review_lists_each_missing_field(self, sample_extracted_fields):
        missing = ["Policy Number", "Asset ID", "Incident Time"]
        result = generate_reasoning("Manual Review", sample_extracted_fields, missing)
        for field in missing:
            assert field in result, f"'{field}' not mentioned in Manual Review reasoning"

    def test_investigation_flag_names_matched_keyword(self, fraud_extracted_fields):
        result = generate_reasoning("Investigation Flag", fraud_extracted_fields, [])
        assert any(kw in result for kw in ["fraud", "staged", "inconsistent"])

    def test_specialist_queue_references_injury(self, injury_claim_fields):
        result = generate_reasoning("Specialist Queue", injury_claim_fields, [])
        assert "injury" in result.lower() or "specialist" in result.lower()

    def test_manual_review_with_single_missing_field(self, sample_extracted_fields):
        result = generate_reasoning("Manual Review", sample_extracted_fields, ["Effective Dates"])
        assert "Effective Dates" in result

    def test_investigation_flag_with_inconsistent_keyword(self, sample_extracted_fields):
        sample_extracted_fields.incidentDescription = (
            "The claimant's story is inconsistent with witness statements."
        )
        result = generate_reasoning("Investigation Flag", sample_extracted_fields, [])
        assert "inconsistent" in result

    def test_standard_processing_does_not_flag_fraud(self, high_value_claim_fields):
        result = generate_reasoning("Standard Processing", high_value_claim_fields, [])
        assert "Investigation Flag" not in result
