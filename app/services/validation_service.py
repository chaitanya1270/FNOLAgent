from typing import List

from app.models.claim_models import ExtractedFields
from app.utils.logger import get_logger

logger = get_logger(__name__)

# All 16 fields listed in the assignment are mandatory.
# List fields (thirdParties, attachments) are treated as missing when empty.
MANDATORY_FIELDS = [
    # Policy Information
    ("policyNumber",        "Policy Number"),
    ("policyholderName",    "Policyholder Name"),
    ("effectiveDates",      "Effective Dates"),
    # Incident Information
    ("incidentDate",        "Incident Date"),
    ("incidentTime",        "Incident Time"),
    ("incidentLocation",    "Incident Location"),
    ("incidentDescription", "Incident Description"),
    # Involved Parties
    ("claimantName",        "Claimant Name"),
    ("thirdParties",        "Third Parties"),
    ("contactDetails",      "Contact Details"),
    # Asset Details
    ("assetType",           "Asset Type"),
    ("assetId",             "Asset ID"),
    ("estimatedDamage",     "Estimated Damage"),
    # Other Mandatory Fields
    ("claimType",           "Claim Type"),
    ("attachments",         "Attachments"),
    ("initialEstimate",     "Initial Estimate"),
]


def validate_claim(fields: ExtractedFields) -> List[str]:
    """Return list of missing mandatory field display names."""
    missing: List[str] = []
    for attr, display_name in MANDATORY_FIELDS:
        value = getattr(fields, attr, None)
        is_missing = (
            value is None
            or (isinstance(value, str) and not value.strip())
            or (isinstance(value, list) and len(value) == 0)
        )
        if is_missing:
            missing.append(display_name)
            logger.debug("Missing mandatory field: %s", display_name)

    if missing:
        logger.info("Validation found %d missing field(s): %s", len(missing), missing)
    else:
        logger.info("Validation passed — all mandatory fields present")

    return missing
