import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from pydantic import BaseModel
from app.services.azure_openai_client import extract_structured_output


class SampleSchema(BaseModel):
    field_a: str = ""
    field_b: int = 0


def _make_mock_response(parsed_obj=None, content=None):
    """Build a mock that mimics openai ChatCompletion response."""
    message = MagicMock()
    message.parsed = parsed_obj
    message.content = content
    choice = MagicMock()
    choice.message = message
    response = MagicMock()
    response.choices = [choice]
    return response


@pytest.mark.asyncio
async def test_successful_structured_output():
    parsed = SampleSchema(field_a="hello", field_b=42)
    mock_response = _make_mock_response(parsed_obj=parsed)

    with patch("app.services.azure_openai_client._build_client") as mock_build:
        mock_client = AsyncMock()
        mock_client.beta.chat.completions.parse = AsyncMock(return_value=mock_response)
        mock_build.return_value = mock_client

        result = await extract_structured_output(
            system_prompt="sys",
            user_prompt="usr",
            response_schema=SampleSchema,
        )

    assert result["field_a"] == "hello"
    assert result["field_b"] == 42


@pytest.mark.asyncio
async def test_fallback_to_raw_json_when_parsed_is_none():
    import json
    raw_json = json.dumps({"field_a": "raw", "field_b": 99})
    mock_response = _make_mock_response(parsed_obj=None, content=raw_json)

    with patch("app.services.azure_openai_client._build_client") as mock_build:
        mock_client = AsyncMock()
        mock_client.beta.chat.completions.parse = AsyncMock(return_value=mock_response)
        mock_build.return_value = mock_client

        result = await extract_structured_output("sys", "usr", SampleSchema)

    assert result["field_a"] == "raw"
    assert result["field_b"] == 99


@pytest.mark.asyncio
async def test_raises_on_empty_response():
    mock_response = _make_mock_response(parsed_obj=None, content=None)

    with patch("app.services.azure_openai_client._build_client") as mock_build:
        mock_client = AsyncMock()
        mock_client.beta.chat.completions.parse = AsyncMock(return_value=mock_response)
        mock_build.return_value = mock_client

        with pytest.raises(Exception):
            await extract_structured_output("sys", "usr", SampleSchema)


@pytest.mark.asyncio
async def test_retries_on_transient_error():
    """Should retry up to 3 times on exception then re-raise."""
    with patch("app.services.azure_openai_client._build_client") as mock_build:
        mock_client = AsyncMock()
        mock_client.beta.chat.completions.parse = AsyncMock(
            side_effect=Exception("transient error")
        )
        mock_build.return_value = mock_client

        with pytest.raises(Exception, match="transient error"):
            await extract_structured_output("sys", "usr", SampleSchema)

        assert mock_client.beta.chat.completions.parse.call_count == 3
