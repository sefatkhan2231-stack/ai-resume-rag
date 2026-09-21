import logging

from fastapi import HTTPException
import ollama
from google import genai
from google.genai import errors as genai_errors
from google.genai import types
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.core.config import get_settings

settings = get_settings()

logger = logging.getLogger(__name__)


def generate_with_ollama(
    system_prompt: str,
    user_prompt: str,
) -> str:

    response = ollama.chat(
        model=settings.OLLAMA_MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        options={
            "temperature": 0,
        },
    )

    return response["message"]["content"]


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(genai_errors.ServerError),
    reraise=True,
)
def generate_with_gemini(
    system_prompt: str,
    user_prompt: str,
    response_schema=None,
) -> str:

    if not settings.GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    client = genai.Client(
        api_key=settings.GEMINI_API_KEY
    )

    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0,
            max_output_tokens=4000,
            response_mime_type="application/json",
            response_schema=response_schema,
            automatic_function_calling=(
                types.AutomaticFunctionCallingConfig(
                    disable=True
                )
            ),
        ),
    )

    if not response.candidates:
        raise RuntimeError(
            "Gemini returned no candidates."
        )

    finish_reason = response.candidates[0].finish_reason
    if finish_reason == "MAX_TOKENS":
        raise RuntimeError(
            "Gemini response was truncated (hit max_output_tokens). "
            "Increase max_output_tokens or shorten the input."
        )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return response.text


def generate(
    system_prompt: str,
    user_prompt: str,
    response_schema=None,
) -> str:

    if settings.LLM_PROVIDER == "gemini":
        try:
            return generate_with_gemini(
                system_prompt,
                user_prompt,
                response_schema=response_schema,
            )
        except genai_errors.ServerError as e:
            logger.exception(
                "Gemini request failed after retries "
                "(provider unavailable)."
            )
            raise HTTPException(
                status_code=503,
                detail="The AI service is temporarily unavailable. Please try again in a moment.",
            ) from e

    return generate_with_ollama(
        system_prompt,
        user_prompt,
    )