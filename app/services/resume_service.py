import os
from uuid import uuid4
from datetime import datetime, timezone
from fastapi import UploadFile, HTTPException
from app.utils.pdf_extractor import extract_text_from_pdf
from app.utils.ocr_extractor import extract_text_via_ocr
from app.models.resume import Resume
from app.db.session import SessionLocal

UPLOAD_DIR = "uploaded_resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

MIN_WORD_COUNT = 60  

MAX_FILE_SIZE_MB = 5  # Limit to 5MB
MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024 

async def process_resume_upload(file: UploadFile, user_id: str):
    contents = await file.read()
    
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size allowed is {MAX_FILE_SIZE_MB}MB."
        )
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    

    file_id = str(uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")

    with open(file_path, "wb") as f:
        f.write(contents)

    # Try normal PDF text extraction
    try:
        extracted_text = extract_text_from_pdf(file_path)
        word_count = len(extracted_text.split())
        if word_count < MIN_WORD_COUNT:
            raise ValueError("Text too short — might need OCR.")
    except Exception:
        # OCR fallback
        try:
            extracted_text = extract_text_via_ocr(file_path)
            word_count = len(extracted_text.split())
            if word_count < MIN_WORD_COUNT:
                raise HTTPException(status_code=500, detail="OCR text is still too short to be useful.")
        except Exception as ocr_error:
            raise HTTPException(status_code=500, detail=f"Text extraction failed. OCR also failed: {ocr_error}")

    # Save to DB
    db = SessionLocal()
    try:
        resume = Resume(
            id=file_id,
            user_id=user_id,
            file_name=file.filename,
            raw_text=extracted_text,
            uploaded_at=datetime.now(timezone.utc),
            parsed_at=None
        )
        db.add(resume)
        db.commit()
        db.refresh(resume)
    finally:
        db.close()

    # Clean up the file
    if os.path.exists(file_path):
        os.remove(file_path)

    return {
        "file_id": file_id,
        "filename": file.filename,
        "extracted_text": extracted_text[:1000]  # Preview
    }
