import json
import os
import re
import uuid
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

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

PROFILES_DIR = Path(__file__).parent / "profiles"
PROFILES_DIR.mkdir(exist_ok=True)


class ProfileSummary(BaseModel):
    id: str
    name: str


@app.get("/api/profiles", response_model=List[ProfileSummary])
async def list_profiles():
    profiles = []
    for f in sorted(PROFILES_DIR.glob("*.json")):
        try:
            data = json.loads(f.read_text())
            profiles.append(ProfileSummary(
                id=f.stem,
                name=data["personal_info"]["full_name"],
            ))
        except (json.JSONDecodeError, KeyError):
            continue
    return profiles


@app.get("/api/profiles/{profile_id}")
async def get_profile(profile_id: str):
    # Sanitize to prevent path traversal
    safe_id = re.sub(r"[^a-zA-Z0-9_-]", "", profile_id)
    file_path = PROFILES_DIR / f"{safe_id}.json"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Profile not found")
    return json.loads(file_path.read_text())


class SaveProfileRequest(BaseModel):
    personal_info: dict
    experiences: list
    education: list


@app.post("/api/profiles")
async def save_profile(request: SaveProfileRequest):
    name = request.personal_info.get("full_name", "unknown")
    safe_name = re.sub(r"[^a-zA-Z0-9]", "_", name).lower().strip("_")
    file_path = PROFILES_DIR / f"{safe_name}.json"
    data = {
        "personal_info": request.personal_info,
        "experiences": request.experiences,
        "education": request.education,
    }
    file_path.write_text(json.dumps(data, indent=2))
    return {"id": safe_name, "name": name}


@app.post("/api/analyze-job", response_model=AnalyzeJobResponse)
async def analyze_job(request: AnalyzeJobRequest):
    try:
        result = await analyze_job_description(
            request.job_description, request.experiences
        )
        # Store selected_skills and is_ai_focused for the generate step
        # These are attached as private attrs by ai_service
        app.state.last_selected_skills = getattr(result, "_selected_skills", {})
        app.state.last_is_ai_focused = getattr(result, "_is_ai_focused", False)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate-resume", response_model=GenerateResumeResponse)
async def generate_resume(request: GenerateResumeRequest):
    try:
        # Retrieve selected skills from the analyze step
        selected_skills = getattr(app.state, "last_selected_skills", None)
        is_ai_focused = getattr(app.state, "last_is_ai_focused", False)

        resume_data = await generate_resume_content(
            request.personal_info,
            request.experiences,
            request.education,
            request.job_description,
            request.extracted_skills,
            selected_skills=selected_skills,
            is_ai_focused=is_ai_focused,
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
