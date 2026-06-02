import json
from typing import Any, Dict, Type

from openai import AsyncAzureOpenAI
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config.settings import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


def _build_client() -> AsyncAzureOpenAI:
    return AsyncAzureOpenAI(
        azure_endpoint=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_api_key,
        api_version=settings.azure_openai_api_version,
        timeout=60.0,
        max_retries=0,  # retries handled by tenacity
    )


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True,
)
async def extract_structured_output(
    system_prompt: str,
    user_prompt: str,
    response_schema: Type[BaseModel],
) -> Dict[str, Any]:
    """Call Azure OpenAI with structured output enforcement and return parsed dict."""
    client = _build_client()
    model = settings.openai_structured_output_model

    logger.info("Calling Azure OpenAI model=%s", model)

    try:
        response = await client.beta.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format=response_schema,
            temperature=0,
        )

        message = response.choices[0].message
        if message.parsed:
            logger.info("Structured output parsed successfully")
            return message.parsed.model_dump()

        # Fallback: parse raw JSON content
        if message.content:
            logger.warning("Falling back to raw JSON parsing")
            return json.loads(message.content)

        raise ValueError("Empty response from Azure OpenAI")

    except Exception as exc:
        logger.error("Azure OpenAI call failed: %s", exc)
        raise
