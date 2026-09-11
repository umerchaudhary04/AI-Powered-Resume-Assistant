import io, re, pdfplumber, docx
from typing import Dict, Tuple

SECTION_HEADERS = {
    "summary": r"(summary|professional summary|profile|objective)",
    "experience": r"(experience|work experience|employment history)",
    "education": r"(education|academic background)",
    "skills": r"(skills|technical skills)",
}

def parse_resume(file_bytes: bytes, filename: str) -> Tuple[str, Dict[str, str]]:
    ext = filename.split(".")[-1].lower()
    if ext == "pdf":
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            raw_text = "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])
    elif ext in ["docx", "doc"]:
        doc = docx.Document(io.BytesIO(file_bytes))
        raw_text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    else:
        raise ValueError("Unsupported format")
    return raw_text, {"general": raw_text} # Simplified for testing
