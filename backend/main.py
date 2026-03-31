import os
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from models import (
    AnalyzeJobRequest,
    AnalyzeJobResponse,
    GenerateResumeRequest,
    GenerateResumeResponse,
)
from services.ai_service import analyze_job_description, generate_resume_content
from services.resume_generator import generate_docx, generate_pdf

app = FastAPI(title="ATS Resume Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GENERATED_DIR = Path(__file__).parent / "generated"
GENERATED_DIR.mkdir(exist_ok=True)


@app.post("/api/analyze-job", response_model=AnalyzeJobResponse)
async def analyze_job(request: AnalyzeJobRequest):
    try:
        result = await analyze_job_description(
            request.job_description, request.experiences
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate-resume", response_model=GenerateResumeResponse)
async def generate_resume(request: GenerateResumeRequest):
    try:
        resume_data = await generate_resume_content(
            request.personal_info,
            request.experiences,
            request.education,
            request.job_description,
            request.extracted_skills,
        )
        # Generate unique filename
        unique_id = uuid.uuid4().hex[:8]
        safe_name = request.personal_info.full_name.replace(" ", "_")
        filename = f"{safe_name}_{unique_id}"

        # Generate DOCX
        docx_path = GENERATED_DIR / f"{filename}.docx"
        generate_docx(resume_data, docx_path)

        # Generate PDF
        pdf_path = GENERATED_DIR / f"{filename}.pdf"
        generate_pdf(resume_data, pdf_path)

        resume_data.filename = filename
        return resume_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/download/{filename}")
async def download_file(filename: str, format: str = "pdf"):
    ext = "pdf" if format == "pdf" else "docx"
    file_path = GENERATED_DIR / f"{filename}.{ext}"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    media_type = (
        "application/pdf"
        if ext == "pdf"
        else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    return FileResponse(
        path=str(file_path),
        filename=f"{filename}.{ext}",
        media_type=media_type,
    )
