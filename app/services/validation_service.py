from typing import List

from app.models.claim_models import ExtractedFields
from app.utils.logger import get_logger

logger = get_logger(__name__)

MANDATORY_FIELDS = [
    ("policyNumber", "Policy Number"),
    ("claimType", "Claim Type"),
    ("incidentDate", "Incident Date"),
    ("estimatedDamage", "Estimated Damage"),
    ("claimantName", "Claimant Name"),
]


def validate_claim(fields: ExtractedFields) -> List[str]:
    """Return list of missing mandatory field display names."""
    missing: List[str] = []
    for attr, display_name in MANDATORY_FIELDS:
        value = getattr(fields, attr, None)
        if not value or (isinstance(value, str) and not value.strip()):
            missing.append(display_name)
            logger.debug("Missing mandatory field: %s", display_name)

    if missing:
        logger.info("Validation found %d missing field(s): %s", len(missing), missing)
    else:
        logger.info("Validation passed — all mandatory fields present")

    return missing
