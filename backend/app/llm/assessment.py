import json

from app.services.llm_service import generate


def generate_candidate_assessment(prompt: str) -> dict:

    content = generate(
        system_prompt="""
You are a strict resume screening assistant.

Use ONLY the verified requirements provided by the user.

Return ONLY valid JSON.

Do not mention any skill that is not present in
MATCHED REQUIREMENTS or MISSING REQUIREMENTS.

Do not infer skills.

Do not invent experience.

Do not mention any technology, skill, experience,
or qualification unless it appears in the supplied
MATCHED REQUIREMENTS or MISSING REQUIREMENTS.
""",
        user_prompt=prompt,
    )

    content = content.strip()

    return json.loads(content)