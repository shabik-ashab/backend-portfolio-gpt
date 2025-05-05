import os
from uuid import uuid4
from datetime import datetime
from fastapi import UploadFile, HTTPException
from app.utils.pdf_extractor import extract_text_from_pdf
from app.models.resume import Resume
from app.db.session import SessionLocal

UPLOAD_DIR = "uploaded_resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def process_resume_upload(file: UploadFile, user_id: str):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    file_id = str(uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")

    with open(file_path, "wb") as f:
        content = file.file.read()
        f.write(content)

    try:
        extracted_text = extract_text_from_pdf(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    db = SessionLocal()
    resume = Resume(
        id=file_id,
        user_id=user_id,  # Set the user_id here
        file_name=file.filename,
        raw_text=extracted_text,
        uploaded_at=datetime.utcnow(),
        parsed_at=None
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    db.close()

    # Clean up the uploaded file after processing
    if os.path.exists(file_path):
        os.remove(file_path)

    return {
        "file_id": file_id,
        "filename": file.filename,
        "extracted_text": extracted_text[:1000]  # Limit preview to first 1000 characters
    }
