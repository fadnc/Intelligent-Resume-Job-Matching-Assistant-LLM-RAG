from fastapi import APIRouter, UploadFile, File, Form
from backend.services.pipeline import analyze_resume
from fastapi.responses import StreamingResponse
import json

router = APIRouter()

@router.post("/analyze")
async def analyze(
    resume : UploadFile = File(...),
    job_description: str = Form(...)
):
    from fastapi import BackgroundTasks
    result = await analyze_resume(resume, job_description)
    return result