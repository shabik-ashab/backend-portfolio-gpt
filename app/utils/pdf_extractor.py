import fitz  # PyMuPDF
from pathlib import Path

def extract_text_from_pdf(file_path: str) -> str:
    if not Path(file_path).exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")
    
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    
    return text.strip()
