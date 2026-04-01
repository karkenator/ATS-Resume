# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ATS Resume Generator — a full-stack app that takes a user's personal info, work experience, and education, analyzes a target job description using Claude AI, and produces tailored, ATS-friendly resumes in PDF and DOCX formats.

## Architecture

**Backend** (`backend/`): Python/FastAPI server on port 8000.
- `main.py` — API routes and FastAPI app setup. Stores generated files in `backend/generated/` and user profiles in `backend/profiles/` (JSON files on disk).
- `models.py` — Pydantic models shared across services (request/response schemas).
- `services/ai_service.py` — Claude API integration (Anthropic SDK). Two calls: `analyze_job_description` (skill extraction + matching + AI-focus detection) and `generate_resume_content` (resume generation with dynamic bullet counts). Uses `claude-sonnet-4-20250514`.
- `services/resume_generator.py` — Generates DOCX (python-docx) and PDF (ReportLab). Font: Calibri (DOCX) / Helvetica (PDF).
- `backend/data/master_skills.json` — Static master skills catalog (10 categories, ~220 skills). Skills are selected from this list based on job description matching.

**Frontend** (`frontend/`): React 19 + Vite + Tailwind CSS v4. Runs on port 5173, proxies `/api` to backend.
- `src/App.jsx` — Main wizard with 5 steps: Personal Info → Experience → Education → Job Description → Preview & Export.
- `src/components/` — Step-specific form components, resume preview, skills preview, export buttons, profile management.

## Commands

```bash
# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload              # runs on :8000

# Frontend
cd frontend
npm install
npm run dev                            # runs on :5173 (proxies /api → :8000)
npm run build                          # production build
```

## Key Design Details

- The Vite dev server proxies `/api` requests to `http://localhost:8000` (configured in `vite.config.js`).
- CORS is configured to allow `http://localhost:5173` only.
- Resume styling defined in `.claude/resume-style.md`. Single font: Calibri (DOCX) / Helvetica (PDF). Compact ATS-friendly formatting.
- **2-page layout:** Page 1 = name/title/contact/profile/skills + first experience (dynamic bullet count fills remaining space). Page 2 = remaining experiences + education.
- **Smart skill selection from master list:** `backend/data/master_skills.json` has ~220 skills across 10 categories. Skills are NOT dumped wholesale — core frameworks from JS/TS and Python are always included, plus job-matched skills from all categories. AI category scales with job focus. See `_select_skills_from_master()` in `ai_service.py`.
- Bullet points: 25-30 words each, real-world hands-on project-based, bold keywords. First experience bullets are dynamic (fills page 1). Subsequent experiences get 7-10 bullets (fills page 2). Older companies weave in modern tech context.
- Profile save/load uses file-based JSON storage in `backend/profiles/`, keyed by sanitized name.
- The `ANTHROPIC_API_KEY` env var must be set for the AI service to work.
