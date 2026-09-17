import re

EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

# Loosely matches common phone formats: +1 555-123-4567, (555) 123 4567, 01712345678, etc.
PHONE_PATTERN = re.compile(r"(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?){2,4}\d{2,4}")


def extract_email(text: str) -> str | None:
    match = EMAIL_PATTERN.search(text)
    return match.group(0) if match else None


def extract_phone(text: str) -> str | None:
    for candidate in PHONE_PATTERN.finditer(text):
        digits = re.sub(r"\D", "", candidate.group(0))
        # Real phone numbers are ~7-15 digits; this filters out stray
        if 7 <= len(digits) <= 15:
            return candidate.group(0).strip()
    return None


def extract_name(text: str) -> str | None:

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if EMAIL_PATTERN.search(line) or PHONE_PATTERN.search(line):
            return None
        if len(line.split()) > 6 or line.isupper():
            return None
        return line
    return None