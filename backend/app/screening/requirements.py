import json

from app.services.llm_service import generate


def extract_job_requirements(job_description: str) -> dict:

    prompt = f"""
You are a job description analysis assistant.

Extract EVERY explicit requirement from the job description.

Return ONLY valid JSON with exactly this structure:

{{
    "skills": [],
    "tools": [],
    "frameworks": [],
    "databases": [],
    "soft_skills": []
}}

Rules:
- Extract EVERY explicit requirement.
- Never infer or add implied requirements.
- Do not merge related requirements.
- soft_skills must only contain explicitly stated soft skills.
- Do not add explanations outside the JSON.

JOB DESCRIPTION:

{job_description}
"""

    content = generate(
        system_prompt=(
            "You extract structured job requirements. "
            "Return valid JSON only."
        ),
        user_prompt=prompt,
    )

    print("===== REQUIREMENTS LLM RESPONSE =====")
    print(repr(content))
    print("===== END REQUIREMENTS RESPONSE =====")

    content = content.strip()

    return json.loads(content)


def flatten_requirements(requirements: dict) -> list:

    flat = []

    for items in requirements.values():

        for item in items:

            item = item.strip()

            if item:
                flat.append(item)

    return list(dict.fromkeys(flat))