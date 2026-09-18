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
- Extract EVERY explicit requirement, never infer or add implied ones.
- Do not merge related requirements (e.g. "PyTorch" and "TensorFlow" stay separate).
- soft_skills: only include skills explicitly stated, do not add common workplace skills.
- Do not add explanations outside the JSON.

JOB DESCRIPTION:
{job_description}
"""
    content = generate(
        system_prompt=(
            "You extract structure job requirements."
            "Return valid JSON only."
        ),
        user_prompt=prompt,
    )
    return json.loads(content)


def flatten_requirements(requirements: dict) -> list:
    flat = []
    for items in requirements.values():
        for item in items:
            item = item.strip()
            if item:
                flat.append(item)
    return list(dict.fromkeys(flat))