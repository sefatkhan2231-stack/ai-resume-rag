import json
from typing import TypedDict

from app.services.llm_service import generate


class JobRequirements(TypedDict):
    skills: list[str]
    tools: list[str]
    frameworks: list[str]
    databases: list[str]
    soft_skills: list[str]


def extract_job_requirements(
    job_description: str
) -> JobRequirements:

    prompt = f"""
Extract EVERY explicit requirement from this job description.

Rules:
- Only extract requirements explicitly stated.
- Never infer requirements.
- Do not add implied skills.
- Do not merge unrelated requirements.
- Put programming languages and technical concepts in skills.
- Put named development tools in tools.
- Put frameworks/libraries in frameworks.
- Put databases in databases.
- Put explicitly stated soft skills in soft_skills.

JOB DESCRIPTION:

{job_description}
"""

    content = generate(
        system_prompt=(
            "You extract structured job requirements "
            "from job descriptions."
        ),
        user_prompt=prompt
    )

    print("===== REQUIREMENTS LLM RESPONSE =====")
    print(content)
    print("===== END REQUIREMENTS RESPONSE =====")

    return json.loads(content)


def flatten_requirements(
    requirements: JobRequirements
) -> list[str]:

    flat = []

    for items in requirements.values():

        for item in items:

            item = item.strip()

            if item:
                flat.append(item)

    return list(dict.fromkeys(flat))