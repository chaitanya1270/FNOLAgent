from typing import List

from app.models.claim_models import ExtractedFields
from app.utils.helpers import extract_numeric_value, safe_lower
from app.utils.logger import get_logger

logger = get_logger(__name__)

FRAUD_KEYWORDS = {"fraud", "inconsistent", "staged"}


def generate_reasoning(
    route: str,
    fields: ExtractedFields,
    missing_fields: List[str],
) -> str:
    """Produce a human-readable explanation for the routing decision."""

    if route == "Investigation Flag":
        description = safe_lower(fields.incidentDescription)
        matched = [kw for kw in FRAUD_KEYWORDS if kw in description]
        keyword_str = ", ".join(f"'{k}'" for k in matched)
        return (
            f"Claim routed to Investigation Flag because the incident description "
            f"contains the keyword(s) {keyword_str}, which may indicate a fraudulent "
            f"or staged claim requiring further investigation."
        )

    if route == "Manual Review":
        field_str = ", ".join(missing_fields)
        return (
            f"Claim routed to Manual Review because the following mandatory field(s) "
            f"are missing or incomplete: {field_str}. A human adjuster must complete "
            f"the information before processing can continue."
        )

    if route == "Specialist Queue":
        return (
            f"Claim routed to Specialist Queue because the claim type is "
            f"'{fields.claimType}', which involves bodily injury. This requires "
            f"review by a specialist adjuster trained in injury claims."
        )

    if route == "Fast-track":
        damage = extract_numeric_value(fields.estimatedDamage)
        return (
            f"Claim routed to Fast-track because the estimated damage "
            f"(${damage:,.2f}) is below the $25,000 threshold, qualifying it "
            f"for expedited automated processing."
        )

    return (
        "Claim routed to Standard Processing. All mandatory fields are present, "
        "no fraud indicators detected, no injury claim, and the estimated damage "
        "meets or exceeds the fast-track threshold."
    )
