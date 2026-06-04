import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from pydantic import BaseModel

from app.services.azure_openai_client import extract_structured_output

PATCH_TARGET = "app.services.azure_openai_client._build_client"


# ---------------------------------------------------------------------------
# Test schema — intentionally different from the main claim schema
# ---------------------------------------------------------------------------
class ClaimSummarySchema(BaseModel):
    claim_id: str = ""
    damage_amount: float = 0.0
    is_urgent: bool = False


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
def _build_response(parsed=None, content=None):
    msg = MagicMock()
    msg.parsed = parsed
    msg.content = content
    choice = MagicMock()
    choice.message = msg
    resp = MagicMock()
    resp.choices = [choice]
    return resp


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------
class TestStructuredOutputSuccess:
    @pytest.mark.asyncio
    async def test_parsed_object_is_returned_as_dict(self):
        parsed = ClaimSummarySchema(claim_id="CLM-001", damage_amount=18200.0, is_urgent=False)
        mock_resp = _build_response(parsed=parsed)

        with patch(PATCH_TARGET) as mock_build:
            mock_client = AsyncMock()
            mock_client.beta.chat.completions.parse = AsyncMock(return_value=mock_resp)
            mock_build.return_value = mock_client

            result = await extract_structured_output("system msg", "user msg", ClaimSummarySchema)

        assert result["claim_id"] == "CLM-001"
        assert result["damage_amount"] == 18200.0
        assert result["is_urgent"] is False

    @pytest.mark.asyncio
    async def test_raw_json_fallback_when_parsed_is_none(self):
        fallback = json.dumps({"claim_id": "CLM-002", "damage_amount": 5000.0, "is_urgent": True})
        mock_resp = _build_response(parsed=None, content=fallback)

        with patch(PATCH_TARGET) as mock_build:
            mock_client = AsyncMock()
            mock_client.beta.chat.completions.parse = AsyncMock(return_value=mock_resp)
            mock_build.return_value = mock_client

            result = await extract_structured_output("sys", "usr", ClaimSummarySchema)

        assert result["claim_id"] == "CLM-002"
        assert result["is_urgent"] is True

    @pytest.mark.asyncio
    async def test_result_is_a_dict(self):
        parsed = ClaimSummarySchema(claim_id="X")
        mock_resp = _build_response(parsed=parsed)

        with patch(PATCH_TARGET) as mock_build:
            mock_client = AsyncMock()
            mock_client.beta.chat.completions.parse = AsyncMock(return_value=mock_resp)
            mock_build.return_value = mock_client

            result = await extract_structured_output("sys", "usr", ClaimSummarySchema)

        assert isinstance(result, dict)


# ---------------------------------------------------------------------------
# Error / edge cases
# ---------------------------------------------------------------------------
class TestStructuredOutputErrors:
    @pytest.mark.asyncio
    async def test_raises_when_both_parsed_and_content_are_none(self):
        mock_resp = _build_response(parsed=None, content=None)

        with patch(PATCH_TARGET) as mock_build:
            mock_client = AsyncMock()
            mock_client.beta.chat.completions.parse = AsyncMock(return_value=mock_resp)
            mock_build.return_value = mock_client

            with pytest.raises(Exception):
                await extract_structured_output("sys", "usr", ClaimSummarySchema)

    @pytest.mark.asyncio
    async def test_retries_three_times_on_transient_failure(self):
        with patch(PATCH_TARGET) as mock_build:
            mock_client = AsyncMock()
            mock_client.beta.chat.completions.parse = AsyncMock(
                side_effect=ConnectionError("upstream timeout")
            )
            mock_build.return_value = mock_client

            with pytest.raises(ConnectionError):
                await extract_structured_output("sys", "usr", ClaimSummarySchema)

            assert mock_client.beta.chat.completions.parse.call_count == 3

    @pytest.mark.asyncio
    async def test_re_raises_original_exception_type(self):
        with patch(PATCH_TARGET) as mock_build:
            mock_client = AsyncMock()
            mock_client.beta.chat.completions.parse = AsyncMock(
                side_effect=ValueError("bad model response")
            )
            mock_build.return_value = mock_client

            with pytest.raises(ValueError, match="bad model response"):
                await extract_structured_output("sys", "usr", ClaimSummarySchema)
