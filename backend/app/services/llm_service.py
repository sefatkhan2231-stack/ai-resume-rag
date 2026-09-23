import logging

import ollama
import requests

from app.core.config import get_settings

settings = get_settings()

logger = logging.getLogger(__name__)


def generate_with_groq(
    system_prompt: str,
    user_prompt: str,
    response_schema: dict | None = None,
) -> str:

    payload = {
        "model": settings.GROQ_MODEL,
        "messages": [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        "temperature": 0,
        "max_tokens": 4096,
        "reasoning_effort": "low",
    }

    if response_schema is not None:
        payload["response_format"] = {
            "type": "json_schema",
            "json_schema": {
                "name": response_schema.get("name", "response"),
                "strict": True,
                "schema": response_schema["schema"],
            },
        }

    response = requests.post(
        f"{settings.GROQ_HOST}/chat/completions",
        headers={
            "Authorization": f"Bearer {settings.GROQ_API_KEY}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]


def generate_with_ollama(
    system_prompt: str,
    user_prompt: str,
) -> str:

    client = ollama.Client(
        host=settings.OLLAMA_HOST
    )

    response = client.chat(
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


def generate(
    system_prompt: str,
    user_prompt: str,
    response_schema=None,
) -> str:

    if settings.LLM_PROVIDER == "groq":
        return generate_with_groq(
            system_prompt,
            user_prompt,
            response_schema=response_schema,
        )

    if settings.LLM_PROVIDER == "ollama":
        return generate_with_ollama(
            system_prompt,
            user_prompt,
        )

    raise ValueError(f"Unknown LLM_PROVIDER: {settings.LLM_PROVIDER!r}")