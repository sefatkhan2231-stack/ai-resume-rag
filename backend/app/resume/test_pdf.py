from pathlib import Path
from backend.app.resume.pdf import extract_pdf_text, clean_text
from backend.app.resume.chunking import extract_sections, chunk_skills, chunk_section

def test_extract_pdf_text():
    pdf_path = Path(__file__).resolve().parent.parent.parent / "dataset" / "sefat_khan.pdf"
    extracted_text = extract_pdf_text(pdf_path)
    cleaned_text = clean_text(extracted_text)
    sections = extract_sections(cleaned_text)

    chunked_skills = chunk_skills(sections.get("SKILLS", ""))

    chunked_sections = []
    for section_name, section_text in sections.items():
        chunked_sections.extend(chunk_section(section_text, section_name))

    print(sections)
    print(chunked_skills)
    print(chunked_sections)

    return chunked_sections

if __name__ == "__main__":
    test_extract_pdf_text()