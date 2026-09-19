import json
import re

from app.services.llm_service import generate


class RequirementExtractionError(RuntimeError):
    """Raised when the LLM response for job requirement extraction can't be parsed as JSON."""


def _extract_json(content: str) -> dict:
   
    if not content or not content.strip():
        raise RequirementExtractionError(
            "LLM returned empty content while extracting job requirements."
        )

    text = content.strip()

    # Strip ```json ... ``` or ``` ... ``` fences if present.
    fence_match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    if fence_match:
        text = fence_match.group(1).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        # Fall back to grabbing the first {...} block in case there's
        # leading/trailing prose around the JSON.
        brace_match = re.search(r"\{.*\}", text, re.DOTALL)
        if brace_match:
            try:
                return json.loads(brace_match.group(0))
            except json.JSONDecodeError:
                pass
        raise RequirementExtractionError(
            f"Could not parse JSON from LLM response: {exc}. Raw content: {content[:500]!r}"
        ) from exc

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
    return _extract_json(content)


def flatten_requirements(requirements: dict) -> list:
    flat = []
    for items in requirements.values():
        for item in items:
            item = item.strip()
            if item:
                flat.append(item)
    return list(dict.fromkeys(flat))