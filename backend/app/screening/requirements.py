import ollama
import json

MODEL_NAME = "llama3.2"

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
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You extract structured job requirements. Return valid JSON only."},
            {"role": "user", "content": prompt},
        ],
        options={"temperature": 0},
    )
    content = response["message"]["content"]
    return json.loads(content)


def flatten_requirements(requirements: dict) -> list:
    flat = []
    for items in requirements.values():
        for item in items:
            item = item.strip()
            if item:
                flat.append(item)
    return list(dict.fromkeys(flat))