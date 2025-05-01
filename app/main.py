from fastapi import FastAPI
from app.routes import resume
from app.routes import auth



app = FastAPI()
app.include_router(resume.router)
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
