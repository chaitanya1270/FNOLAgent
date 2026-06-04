import pytest
from app.models.claim_models import ExtractedFields
from app.services.routing_service import determine_route, ROUTES, FRAUD_KEYWORDS, FAST_TRACK_THRESHOLD


# ---------------------------------------------------------------------------
# Constants sanity
# ---------------------------------------------------------------------------
def test_fast_track_threshold_is_25000():
    assert FAST_TRACK_THRESHOLD == 25_000.0


def test_fraud_keywords_includes_required_terms():
    for word in ("fraud", "inconsistent", "staged"):
        assert word in FRAUD_KEYWORDS


# ---------------------------------------------------------------------------
# Primary routing outcomes
# ---------------------------------------------------------------------------
class TestPrimaryRoutes:
    def test_below_threshold_routes_to_fast_track(self, sample_extracted_fields):
        """$18,200 < $25,000, all fields present, no fraud → Fast-track."""
        route = determine_route(sample_extracted_fields, [])
        assert route == ROUTES["fast_track"]

    def test_missing_fields_routes_to_manual_review(self, incomplete_claim_fields):
        route = determine_route(incomplete_claim_fields, ["Policy Number", "Effective Dates"])
        assert route == ROUTES["manual_review"]

    def test_fraud_keyword_routes_to_investigation(self, fraud_extracted_fields):
        route = determine_route(fraud_extracted_fields, [])
        assert route == ROUTES["investigation_flag"]

    def test_injury_claim_routes_to_specialist_queue(self, injury_claim_fields):
        route = determine_route(injury_claim_fields, [])
        assert route == ROUTES["specialist_queue"]

    def test_high_damage_routes_to_standard_processing(self, high_value_claim_fields):
        """$62,500 ≥ $25,000, no fraud, no injury → Standard Processing."""
        route = determine_route(high_value_claim_fields, [])
        assert route == ROUTES["standard"]


# ---------------------------------------------------------------------------
# Priority ordering
# ---------------------------------------------------------------------------
class TestRoutingPriority:
    def test_fraud_beats_missing_fields(self, fraud_extracted_fields):
        route = determine_route(fraud_extracted_fields, ["Policy Number", "Asset ID"])
        assert route == ROUTES["investigation_flag"]

    def test_fraud_beats_injury(self):
        fields = ExtractedFields(
            policyNumber="POL-999",
            claimType="injury",
            incidentDate="11/03/2025",
            estimatedDamage="$5,000",
            claimantName="Test User",
            incidentDescription="This was clearly a staged accident involving fraud.",
        )
        route = determine_route(fields, [])
        assert route == ROUTES["investigation_flag"]

    def test_fraud_beats_fast_track(self, fraud_extracted_fields):
        fraud_extracted_fields.estimatedDamage = "$1,000"
        route = determine_route(fraud_extracted_fields, [])
        assert route == ROUTES["investigation_flag"]

    def test_missing_fields_beats_specialist_queue(self):
        fields = ExtractedFields(
            claimType="injury",
            incidentDate="11/03/2025",
            estimatedDamage="$5,000",
            claimantName="Test User",
        )
        route = determine_route(fields, ["Policy Number"])
        assert route == ROUTES["manual_review"]

    def test_specialist_queue_beats_fast_track(self, injury_claim_fields):
        injury_claim_fields.estimatedDamage = "$10,000"
        route = determine_route(injury_claim_fields, [])
        assert route == ROUTES["specialist_queue"]


# ---------------------------------------------------------------------------
# Fraud keyword variations
# ---------------------------------------------------------------------------
class TestFraudKeywords:
    @pytest.mark.parametrize("keyword", ["fraud", "inconsistent", "staged"])
    def test_each_keyword_triggers_investigation(self, keyword, sample_extracted_fields):
        sample_extracted_fields.incidentDescription = f"The claim appears to be {keyword}."
        route = determine_route(sample_extracted_fields, [])
        assert route == ROUTES["investigation_flag"]

    def test_uppercase_fraud_keyword_detected(self, sample_extracted_fields):
        sample_extracted_fields.incidentDescription = "FRAUD suspected based on evidence."
        route = determine_route(sample_extracted_fields, [])
        assert route == ROUTES["investigation_flag"]

    def test_no_fraud_keyword_does_not_flag(self, sample_extracted_fields):
        sample_extracted_fields.incidentDescription = "Genuine accident with no suspicious indicators."
        route = determine_route(sample_extracted_fields, [])
        assert route != ROUTES["investigation_flag"]

    def test_none_description_does_not_crash(self, sample_extracted_fields):
        sample_extracted_fields.incidentDescription = None
        route = determine_route(sample_extracted_fields, [])
        assert route != ROUTES["investigation_flag"]


# ---------------------------------------------------------------------------
# Damage threshold edge cases
# ---------------------------------------------------------------------------
class TestDamageThreshold:
    def test_exactly_at_threshold_is_not_fast_track(self, sample_extracted_fields):
        sample_extracted_fields.estimatedDamage = "$25,000"
        route = determine_route(sample_extracted_fields, [])
        assert route == ROUTES["standard"]

    def test_one_dollar_below_threshold_is_fast_track(self, sample_extracted_fields):
        sample_extracted_fields.estimatedDamage = "$24,999"
        route = determine_route(sample_extracted_fields, [])
        assert route == ROUTES["fast_track"]

    def test_unparseable_damage_falls_to_standard(self, sample_extracted_fields):
        sample_extracted_fields.estimatedDamage = "unknown"
        route = determine_route(sample_extracted_fields, [])
        assert route == ROUTES["standard"]

    def test_none_damage_falls_to_standard(self, sample_extracted_fields):
        sample_extracted_fields.estimatedDamage = None
        route = determine_route(sample_extracted_fields, [])
        assert route == ROUTES["standard"]
