import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.pdf_extractor import extract_text_from_pdf
from uuid import uuid4

router = APIRouter()

UPLOAD_DIR = "uploaded_resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    # Ensure upload directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Save the uploaded file temporarily
    file_id = str(uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Extract text from the PDF
    try:
        extracted_text = extract_text_from_pdf(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "file_id": file_id,
        "filename": file.filename,
        "extracted_text": extracted_text[:1000]  # limit for preview
    }

