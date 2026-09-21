import logging

import ollama

from app.core.config import get_settings

settings = get_settings()

logger = logging.getLogger(__name__)


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

    return generate_with_ollama(
        system_prompt,
        user_prompt,
    )