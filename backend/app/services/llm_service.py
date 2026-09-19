import json

import ollama

from google import genai

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

def generate_with_gemini(
    system_prompt: str,
    user_prompt: str,
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
        config={
            "system_instruction": system_prompt,
            "temperature": 0,
            "max_output_tokens": 1000,
        },
    )

    return response.text

def generate(
        system_prompt: str,
        user_prompt: str,
) -> str:

    if settings.LLM_PROVIDER == "gemini":
        return generate_with_gemini(
            system_prompt,
            user_prompt,
        )

    return generate_with_ollama(
        system_prompt,
        user_prompt,
    )