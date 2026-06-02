from typing import List, Optional

from app.models.claim_models import ExtractedFields
from app.utils.helpers import extract_numeric_value, safe_lower
from app.utils.logger import get_logger

logger = get_logger(__name__)

FRAUD_KEYWORDS = {"fraud", "inconsistent", "staged"}
FAST_TRACK_THRESHOLD = 25_000.0

ROUTES = {
    "investigation_flag": "Investigation Flag",
    "manual_review": "Manual Review",
    "specialist_queue": "Specialist Queue",
    "fast_track": "Fast-track",
    "standard": "Standard Processing",
}


def determine_route(fields: ExtractedFields, missing_fields: List[str]) -> str:
    """Apply routing rules in priority order and return the recommended route."""

    # Priority 1 — Investigation Flag
    description = safe_lower(fields.incidentDescription)
    if any(keyword in description for keyword in FRAUD_KEYWORDS):
        logger.info("Route: Investigation Flag (fraud keyword detected)")
        return ROUTES["investigation_flag"]

    # Priority 2 — Manual Review
    if missing_fields:
        logger.info("Route: Manual Review (missing fields: %s)", missing_fields)
        return ROUTES["manual_review"]

    # Priority 3 — Specialist Queue
    claim_type = safe_lower(fields.claimType)
    if "injury" in claim_type:
        logger.info("Route: Specialist Queue (injury claim)")
        return ROUTES["specialist_queue"]

    # Priority 4 — Fast-track
    damage_amount = extract_numeric_value(fields.estimatedDamage)
    if damage_amount is not None and damage_amount < FAST_TRACK_THRESHOLD:
        logger.info("Route: Fast-track (damage $%.2f < $25,000)", damage_amount)
        return ROUTES["fast_track"]

    # Priority 5 — Standard Processing
    logger.info("Route: Standard Processing")
    return ROUTES["standard"]
