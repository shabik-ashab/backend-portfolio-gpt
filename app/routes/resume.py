from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.services.resume_service import process_resume_upload
from app.utils.auth import get_current_user
from app.models.user import User 

router = APIRouter()

@router.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    # Pass the user_id to the service function
    return process_resume_upload(file, user_id=current_user.id)
