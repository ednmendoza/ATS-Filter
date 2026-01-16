import io
from typing import Dict, Any, Optional
import pypdf
from docx import Document


def parse_pdf(file_content: bytes) -> str:
    """Extract plain text from PDF"""
    pdf_file = io.BytesIO(file_content)
    reader = pypdf.PdfReader(pdf_file)
    text_parts = []
    
    for page in reader.pages:
        text_parts.append(page.extract_text())
    
    return "\n".join(text_parts)


def parse_docx(file_content: bytes) -> str:
    """Extract plain text from DOCX"""
    docx_file = io.BytesIO(file_content)
    doc = Document(docx_file)
    text_parts = []
    
    for paragraph in doc.paragraphs:
        text_parts.append(paragraph.text)
    
    return "\n".join(text_parts)


def parse_txt(file_content: bytes) -> str:
    """Extract plain text from TXT"""
    return file_content.decode('utf-8', errors='ignore')


def parse_resume(file_content: bytes, filename: str) -> Dict[str, Any]:
    """
    Parse resume file and return structured data.
    Returns plain text for MVP - structured parsing can be added later.
    """
    filename_lower = filename.lower()
    
    if filename_lower.endswith('.pdf'):
        raw_text = parse_pdf(file_content)
    elif filename_lower.endswith('.docx'):
        raw_text = parse_docx(file_content)
    elif filename_lower.endswith('.txt'):
        raw_text = parse_txt(file_content)
    else:
        raise ValueError(f"Unsupported file format: {filename}")
    
    # MVP: Return raw text, structured parsing can be added later
    return {
        "raw_text": raw_text,
        "parsed_json": None  # Can be enhanced with structured extraction later
    }
