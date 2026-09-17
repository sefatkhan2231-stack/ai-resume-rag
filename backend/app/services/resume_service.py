import uuid
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.resume.pdf import extract_pdf_text, clean_text
from app.resume.chunking import extract_sections, chunk_section
from app.resume.contact import extract_email, extract_phone
from app.rag.vector_store import index_chunks
from app.models.candidate import Candidate
from app.resume.name_extraction import extract_candidate_name


class ResumeProcessingError(Exception):
    """Raised for invalid/corrupted uploads -- lets the route report a
    clean per-file error instead of a raw 500, per the "handle invalid
    files gracefully" requirement."""


def _save_upload(file: UploadFile, upload_dir: str) -> Path:
    Path(upload_dir).mkdir(parents=True, exist_ok=True)
    destination = Path(upload_dir) / file.filename
    with destination.open("wb") as f:
        f.write(file.file.read())
    return destination


def process_resume(file: UploadFile, settings: Settings, db: Session) -> Candidate:

    resume_id = f"resume_{uuid.uuid4().hex[:8]}"
    candidate_id = f"candidate_{uuid.uuid4().hex[:8]}"

    saved_path = _save_upload(file, settings.UPLOAD_DIR)

    try:
        raw_text = extract_pdf_text(str(saved_path))
    except Exception as exc:
        raise ResumeProcessingError(f"Could not read '{file.filename}' as a PDF.") from exc

    if not raw_text.strip():
        raise ResumeProcessingError(f"'{file.filename}' contains no extractable text.")

    cleaned = clean_text(raw_text)
    sections = extract_sections(cleaned)

    chunks = []
    for section_name, section_text in sections.items():
        chunks.extend(chunk_section(section_text, section_name))

    if not chunks:
        raise ResumeProcessingError(
            f"'{file.filename}' didn't match any expected resume sections."
        )

    chunks_indexed = index_chunks(chunks, resume_id=resume_id, candidate_id=candidate_id)

    candidate = Candidate(
        candidate_id=candidate_id,
        resume_id=resume_id,
        filename=file.filename,
        name=extract_candidate_name(cleaned),
        email=extract_email(cleaned),
        phone=extract_phone(cleaned),
        chunks_indexed=chunks_indexed,
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return candidate