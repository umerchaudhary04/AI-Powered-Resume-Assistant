import io
import re
from typing import Dict, Tuple
import pdfplumber
import docx

SECTION_HEADERS = {
    "summary": r"(summary|professional summary|profile|objective)",
    "experience": r"(experience|work experience|employment history|professional experience)",
    "education": r"(education|academic background)",
    "skills": r"(skills|technical skills|core competencies)",
    "projects": r"(projects|key projects)",
}

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extracts raw text from a PDF file buffer."""
    text_chunks = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text_chunks.append(extracted)
    full_text = "\n".join(text_chunks).strip()
    if not full_text:
        raise ValueError("Unable to extract text. The document might be scanned or image-based.")
    return full_text

def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extracts raw text from a DOCX file buffer."""
    doc = docx.Document(io.BytesIO(file_bytes))
    full_text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()]).strip()
    if not full_text:
        raise ValueError("The uploaded DOCX file contains no readable text.")
    return full_text

def parse_resume(file_bytes: bytes, filename: str) -> Tuple[str, Dict[str, str]]:
    """Extracts text and segments it into common resume sections."""
    ext = filename.split(".")[-1].lower()
    if ext == "pdf":
        raw_text = extract_text_from_pdf(file_bytes)
    elif ext in ["docx", "doc"]:
        raw_text = extract_text_from_docx(file_bytes)
    else:
        raise ValueError(f"Unsupported file format: .{ext}")

    lines = raw_text.split("\n")
    sections: Dict[str, list] = {"contact": [], "general": []}
    current_section = "contact"

    for line in lines:
        cleaned_line = line.strip()
        matched_section = None
        for sec, pattern in SECTION_HEADERS.items():
            if re.match(rf"^(?:#+\s*)?{pattern}[:\s]*$", cleaned_line, re.IGNORECASE):
                matched_section = sec
                break
        
        if matched_section:
            current_section = matched_section
            if current_section not in sections:
                sections[current_section] = []
        else:
            sections.setdefault(current_section, []).append(cleaned_line)

    segmented = {sec: "\n".join(content).strip() for sec, content in sections.items() if content}
    return raw_text, segmented
