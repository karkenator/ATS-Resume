import json
import os
from typing import Dict, List, Optional

import anthropic

from models import (
    AnalyzeJobResponse,
    BulletPoint,
    Education,
    ExperienceOutput,
    GenerateResumeResponse,
    JobDescription,
    Experience,
    PersonalInfo,
)

client = anthropic.AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))


async def analyze_job_description(
    job_description: JobDescription, experiences: List[Experience]
) -> AnalyzeJobResponse:
    experience_text = "\n".join(
        f"- {exp.role} at {exp.company_name} ({exp.start_date} - {exp.end_date}): {exp.description or 'N/A'}"
        for exp in experiences
    )

    prompt = f"""Analyze this job description and extract skills, then match them against the candidate's experience.

JOB DESCRIPTION:
Company: {job_description.company_name}
Title: {job_description.job_title}
Description:
{job_description.description}

CANDIDATE EXPERIENCE:
{experience_text}

Return a JSON object with exactly this structure:
{{
  "extracted_skills": {{
    "Programming Languages": ["Python", "JavaScript", ...],
    "Frameworks & Libraries": ["React", "FastAPI", ...],
    "Cloud & DevOps": ["AWS", "Docker", ...],
    "Database": ["PostgreSQL", "MongoDB", ...],
    "Others": ["Git", "Agile", ...]
  }},
  "matched_skills": ["Python", "React", ...],
  "matching_score": 0.85,
  "summary": "A 2-3 sentence professional summary tailored to this job, highlighting the candidate's most relevant experience and skills. Bold-worthy keywords should be noted."
}}

Rules:
- Extract ALL technical skills, tools, methodologies from the job description
- Group them into logical categories
- matched_skills should only include skills the candidate likely has based on their experience
- matching_score is a float 0-1 representing how well the candidate matches
- summary should be compelling, ATS-friendly, and reference specific technologies from the job description
- Return ONLY valid JSON, no markdown fences"""

    response = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )

    result = json.loads(response.content[0].text)
    return AnalyzeJobResponse(**result)


async def generate_resume_content(
    personal_info: PersonalInfo,
    experiences: List[Experience],
    education: List[Education],
    job_description: JobDescription,
    extracted_skills: Optional[Dict[str, List[str]]] = None,
) -> GenerateResumeResponse:
    # Determine bullet counts: most recent gets more
    num_exp = len(experiences)
    if num_exp == 1:
        bullet_counts = [8]
    elif num_exp == 2:
        bullet_counts = [6, 4]
    elif num_exp == 3:
        bullet_counts = [5, 3, 3]
    else:
        bullet_counts = [5] + [3] * (num_exp - 1)

    experience_entries = []
    for i, exp in enumerate(experiences):
        experience_entries.append(
            f"Company {i+1}: {exp.role} at {exp.company_name} ({exp.start_date} - {exp.end_date}), {exp.location}\n"
            f"Description: {exp.description or 'N/A'}\n"
            f"Required bullets: {bullet_counts[i]}"
        )

    skills_context = ""
    if extracted_skills:
        skills_context = "Extracted skills from job description:\n" + json.dumps(
            extracted_skills, indent=2
        )

    prompt = f"""Generate professional resume content tailored to this job description.

JOB DESCRIPTION:
Company: {job_description.company_name}
Title: {job_description.job_title}
Description:
{job_description.description}

{skills_context}

CANDIDATE INFO:
Name: {personal_info.full_name}
Current Title: {personal_info.title}

EXPERIENCES:
{chr(10).join(experience_entries)}

EDUCATION:
{chr(10).join(f"- {edu.degree} at {edu.institution} ({edu.start_date} - {edu.end_date})" for edu in education)}

Return a JSON object with this EXACT structure:
{{
  "summary": "A compelling 2-3 sentence professional summary. Use bold keywords by wrapping them in **double asterisks**.",
  "skills": {{
    "Programming Languages": ["Python", "JavaScript", ...],
    "Frameworks & Libraries": ["React", "Node.js", ...],
    "Database": ["PostgreSQL", ...],
    "Cloud & DevOps": ["AWS", "Docker", ...],
    "Others": ["Git", "Agile", ...]
  }},
  "experiences": [
    {{
      "company_name": "{experiences[0].company_name}",
      "role": "{experiences[0].role}",
      "location": "{experiences[0].location}",
      "period": "{experiences[0].start_date} – {experiences[0].end_date}",
      "bullets": [
        {{
          "text": "Led the development of a microservices architecture using Python and FastAPI, reducing API response times by 40% and improving system scalability across 3 production environments.",
          "bold_keywords": ["Python", "FastAPI", "microservices"]
        }}
      ]
    }}
  ]
}}

CRITICAL RULES FOR BULLET POINTS:
1. Each bullet MUST be exactly 25-30 words (this is ~2 lines on a resume)
2. Start each bullet with a strong past-tense action verb (Led, Developed, Implemented, Architected, etc.)
3. Include specific metrics/numbers where possible (%, time saved, scale)
4. Include technology keywords from the job description naturally
5. bold_keywords should list technologies/tools mentioned in each bullet that match the job description
6. Make bullets sound natural and professional, not keyword-stuffed
7. Company {experiences[0].company_name} gets {bullet_counts[0]} bullets (most recent = most bullets)

CRITICAL RULES FOR SKILLS:
1. Include skills from BOTH the job description AND the candidate's experience
2. Group logically into categories
3. Prioritize skills mentioned in the job description

Return ONLY valid JSON, no markdown fences."""

    response = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
    )

    result = json.loads(response.content[0].text)

    # Build response
    exp_outputs = []
    for exp_data in result["experiences"]:
        bullets = [
            BulletPoint(
                text=b["text"],
                bold_keywords=b.get("bold_keywords", []),
            )
            for b in exp_data["bullets"]
        ]
        exp_outputs.append(
            ExperienceOutput(
                company_name=exp_data["company_name"],
                role=exp_data["role"],
                location=exp_data["location"],
                period=exp_data["period"],
                bullets=bullets,
            )
        )

    return GenerateResumeResponse(
        summary=result["summary"],
        skills=result["skills"],
        experiences=exp_outputs,
        education=education,
        personal_info=personal_info,
        filename="",  # set later by main.py
    )
