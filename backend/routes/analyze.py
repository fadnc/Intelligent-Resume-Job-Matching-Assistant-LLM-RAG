from fastapi import APIRouter, UploadFile, File, Form
from services.pipeline import analyze_resume

router = APIRouter()

@router.post("/analyze")
async def analyze(
    resume : UploadFile = File(...),
    job_description: str = Form(...)
):
    result = await analyze_resume(resume, job_description)
    return result