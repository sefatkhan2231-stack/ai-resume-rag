import re
import ollama

MODEL_NAME = "llama3.2"

SECTION_KEYWORDS = {
    "summary", "objective", "profile", "about", "contact",
    "education", "experience", "skills", "projects", "certifications",
    "awards", "publications", "references", "professional experience",
    "work experience", "technical skills", "personal projects",
}

_EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_PHONE_RE = re.compile(r"(\+?\d[\d\-\s().]{7,}\d)")
_URL_RE = re.compile(r"(https?://|www\.)\S+", re.IGNORECASE)


def _looks_like_name(line: str) -> bool:
    line = line.strip()
    if not line or len(line) > 60:
        return False
    if _EMAIL_RE.search(line) or _PHONE_RE.search(line) or _URL_RE.search(line):
        return False
    if line.lower().strip(":") in SECTION_KEYWORDS:
        return False
    words = line.split()
    if not (1 < len(words) <= 5):
        return False
    for word in words:
        cleaned = word.strip(".,-")
        if not cleaned or not all(ch.isalpha() or ch in "'-." for ch in cleaned):
            return False
    return True


def _heuristic_name(cleaned_text: str) -> str | None:

    lines = [ln.strip() for ln in cleaned_text.splitlines() if ln.strip()]
    for line in lines[:6]:
        if _looks_like_name(line):
            return line
    return None


def _llm_name(cleaned_text: str) -> str | None:

    snippet = cleaned_text[:600]
    prompt = f"""
Extract ONLY the candidate's full name from the top of this resume text.
If no clear name is present, return exactly: UNKNOWN

Resume text:
{snippet}

Return ONLY the name, nothing else, or UNKNOWN.
"""
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "Extract only the candidate's name. No explanation."},
                {"role": "user", "content": prompt},
            ],
            options={"temperature": 0},
        )
        answer = response["message"]["content"].strip()
    except Exception:
        return None

    if not answer or answer.upper() == "UNKNOWN":
        return None

    first_line = answer.splitlines()[0].strip()
    if len(first_line.split()) > 6:
        return None
    return first_line


def extract_candidate_name(cleaned_text: str) -> str:
    return (
        _heuristic_name(cleaned_text)
        or _llm_name(cleaned_text)
        or "Candidate"
    )