import re

SECTION_NAMES = ["ABOUT ME", "SKILLS", "PROFESSIONAL EXPERIENCE", "PROJECTS", "EDUCATION"]


def extract_sections(text: str, section_names=SECTION_NAMES) -> dict:
    pattern = r"(?m)^(" + "|".join(map(re.escape, section_names)) + r")\s*$"
    parts = re.split(pattern, text, flags=re.IGNORECASE)

    sections = {}
    current_section = None
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if part.upper() in section_names:
            current_section = part.upper()
            sections[current_section] = ""
        elif current_section:
            sections[current_section] += " " + part
    return sections


def chunk_skills(content: str) -> list:
    """
    Split SKILLS into individual subsections.
    """

    subsection_patterns = {
        "languages": r"Languages:\s*(.*?)(?=Frontend:|Backend:|Database:|Tools:|Soft Skills:|Communication Skills:|$)",
        "frontend": r"Frontend:\s*(.*?)(?=Backend:|Database:|Tools:|Soft Skills:|Communication Skills:|$)",
        "backend": r"Backend:\s*(.*?)(?=Database:|Tools:|Soft Skills:|Communication Skills:|$)",
        "database": r"Database:\s*(.*?)(?=Tools:|Soft Skills:|Communication Skills:|$)",
        "tools": r"Tools:\s*(.*?)(?=Soft Skills:|Communication Skills:|$)",
        "soft_skills": r"Soft Skills:\s*(.*?)(?=Communication Skills:|$)",
        "communication": r"Communication Skills:\s*(.*?)$",
    }

    chunks = []

    for subsection, pattern in subsection_patterns.items():

        match = re.search(
            pattern,
            content,
            flags=re.IGNORECASE | re.DOTALL
        )

        if not match:
            continue

        text = match.group(1).strip()

        if not text:
            continue

        chunks.append({
            "text": f"SKILLS — {subsection.upper()}\n{text}",
            "section": "SKILLS",
            "subsection": subsection,
        })

    return chunks


def chunk_section(
    text: str,
    section: str,
    max_words: int = 150,
    overlap: int = 30
) -> list:

    if section == "SKILLS":
        return chunk_skills(text)

    words = text.split()

    if len(words) <= max_words:
        return [{
            "text": f"{section}\n{text}",
            "section": section
        }]

    chunks = []

    start = 0

    while start < len(words):

        end = start + max_words

        piece = " ".join(words[start:end])

        chunks.append({
            "text": f"{section}\n{piece}",
            "section": section
        })

        start += max_words - overlap

    return chunks