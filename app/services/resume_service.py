import os
from uuid import uuid4
from datetime import datetime, timezone
from fastapi import UploadFile, HTTPException
from app.utils.pdf_extractor import extract_text_from_pdf
from app.models.resume import Resume
from app.db.session import SessionLocal

UPLOAD_DIR = "uploaded_resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

MAX_RESUMES_PER_USER = 10

def process_resume_upload(file: UploadFile, user_id: str):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    file_id = str(uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")

    # Save the uploaded file temporarily
    with open(file_path, "wb") as f:
        content = file.file.read()
        f.write(content)

    try:
        # Extract text from the PDF
        extracted_text = extract_text_from_pdf(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Save to the database
    db = SessionLocal()

    # Check how many resumes the user has already uploaded
    user_resumes = db.query(Resume).filter(Resume.user_id == user_id).order_by(Resume.uploaded_at.desc()).all()

    # If the user already has 5 resumes, delete the oldest one
    if len(user_resumes) >= MAX_RESUMES_PER_USER:
        oldest_resume = user_resumes[-1]  # The oldest resume is the last in the list
        db.delete(oldest_resume)
        db.commit()

    # Add the new resume to the database
    resume = Resume(
        id=file_id,
        user_id=user_id,  
        file_name=file.filename,
        raw_text=extracted_text,
        uploaded_at = datetime.now(timezone.utc),
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
