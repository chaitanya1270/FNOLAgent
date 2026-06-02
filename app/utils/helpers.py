import re
from typing import Optional


def extract_numeric_value(value: Optional[str]) -> Optional[float]:
    """Parse numeric dollar amount from a string like '$12,500' or '12500'."""
    if not value:
        return None
    cleaned = re.sub(r"[^\d.]", "", value.replace(",", ""))
    try:
        return float(cleaned)
    except (ValueError, TypeError):
        return None


def normalize_text(text: str) -> str:
    """Collapse whitespace and strip text."""
    return re.sub(r"\s+", " ", text).strip()


def safe_lower(value: Optional[str]) -> str:
    """Return lowercase string or empty string for None."""
    return (value or "").lower()
