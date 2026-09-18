import json

import ollama
from huggingface_hub import InferenceClient

from app.core.config import get_settings

settings = get_settings()

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

def generate_with_huggingface(
        system_prompt: str,
        user_prompt: str,
) -> str:

    if not settings.HF_TOKEN:
        raise RuntimeError(
            "HF_TOKEN is not configured."
        )

    client = InferenceClient(
        api_key=settings.HF_TOKEN,
    )

    response = client.chat.completions.create(
        model=settings.HF_MODEL,
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
        temperature=0,
        max_tokens=1000,
    )

    return response.choices[0].message.content

def generate(
        system_prompt: str,
        user_prompt: str,
) -> str:

    if settings.LLM_PROVIDER == "huggingface":
        return generate_with_huggingface(
            system_prompt,
            user_prompt,
        )

    return generate_with_ollama(
        system_prompt,
        user_prompt,
    )