import json
import ollama

MODEL_NAME = "llama3.2"

def generate_candidate_assessment(prompt: str) -> dict:

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": """
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
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={"temperature": 0},
    )

    content = response["message"]["content"].strip()

    return json.loads(content)