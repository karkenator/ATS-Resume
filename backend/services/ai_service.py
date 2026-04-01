import json
import os
from pathlib import Path
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

client = anthropic.AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", "))

# Load master skills from static JSON
_DATA_DIR = Path(__file__).parent.parent / "data"
with open(_DATA_DIR / "master_skills.json") as f:
    MASTER_SKILLS: Dict[str, List[str]] = json.load(f)

# Core JS/TS frameworks — always included regardless of job description
JS_TS_CORE = {
    "React", "Redux", "Node.js", "Express.js", "Next.js", "Jest",
    "Tailwind CSS", "jQuery", "Bootstrap",
}

# Core Python frameworks — always included regardless of job description
PYTHON_CORE = {"Flask", "Django", "FastAPI", "Pytest"}

# Core programming languages — always included
LANG_CORE = {"JavaScript", "TypeScript", "Python", "HTML5", "CSS3"}

# AI category name
AI_CATEGORY = "AI & Machine Learning"
# Minimal AI skills for non-AI jobs
AI_MINIMAL = ["RAG", "LangChain", "Prompt Engineering", "Large Language Models", "OpenAI"]


def _parse_json_response(text: str) -> dict:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        lines = [l for l in lines[1:] if l.strip() != "```"]
        cleaned = "\n".join(lines)
    return json.loads(cleaned)


def _estimate_skill_lines(skills: Dict[str, List[str]]) -> int:
    """Estimate how many rendered lines the skills section occupies.

    At 10.5pt Calibri with 7.5" usable width (~85 chars/line), each category
    line = "Category: skill1, skill2, ..." wrapping as needed.
    """
    total = 0
    for category, skill_list in skills.items():
        text = f"{category}: {', '.join(skill_list)}"
        total += max(1, -(-len(text) // 85))  # ceiling division
    return total


MIN_SKILLS_PER_CATEGORY = 3  # Never show a category with fewer than 3 skills


def _pad_category(selected: List[str], master_list: List[str], minimum: int = MIN_SKILLS_PER_CATEGORY) -> List[str]:
    """If a category has fewer than `minimum` skills, pad with more from master list."""
    if len(selected) >= minimum:
        return selected
    seen = {s.lower() for s in selected}
    for s in master_list:
        if s.lower() not in seen:
            selected.append(s)
            seen.add(s.lower())
            if len(selected) >= minimum:
                break
    return selected


def _select_skills_from_master(
    extracted_skills: Dict[str, List[str]],
    is_ai_focused: bool,
) -> Dict[str, List[str]]:
    """Select relevant skills from the master list based on job description.

    Strategy:
    - Programming Languages: always include core (JS, TS, Python, HTML5, CSS3) + job-matched
    - JS/TS: always include core frameworks + job-matched from full list
    - Python/Go/Ruby: always include core frameworks + job-matched
    - AI: full if AI-focused, minimal subset otherwise
    - All other categories: only job-matched skills (padded to minimum 3)
    - Categories are reordered so the most job-relevant ones appear first
    """
    # Flatten extracted skills for matching
    extracted_flat = set()
    for skills in extracted_skills.values():
        extracted_flat.update(s.lower() for s in skills)

    result = {}

    for category, master_list in MASTER_SKILLS.items():
        if category == "Programming Languages":
            selected = [s for s in master_list if s in LANG_CORE or s.lower() in extracted_flat]
            result[category] = _pad_category(selected, master_list)
            continue

        if category == "JavaScript & TypeScript":
            selected = []
            seen = set()
            for s in master_list:
                if s in JS_TS_CORE or s.lower() in extracted_flat:
                    if s.lower() not in seen:
                        selected.append(s)
                        seen.add(s.lower())
            result[category] = selected  # core already ensures enough
            continue

        if category == "Python, Go (Golang), Ruby":
            selected = []
            seen = set()
            for s in master_list:
                if s in PYTHON_CORE or s.lower() in extracted_flat:
                    if s.lower() not in seen:
                        selected.append(s)
                        seen.add(s.lower())
            result[category] = selected  # core already ensures enough
            continue

        if category == AI_CATEGORY:
            if is_ai_focused:
                result[category] = list(master_list)
            else:
                result[category] = list(AI_MINIMAL)
            continue

        if category == "Soft Skills":
            matched = [s for s in master_list if s.lower() in extracted_flat]
            if not matched:
                matched = master_list[:6]
            result[category] = _pad_category(matched[:8], master_list, minimum=5)
            continue

        # All other categories: only job-matched, padded to minimum 3
        matched = [s for s in master_list if s.lower() in extracted_flat]
        if matched:
            result[category] = _pad_category(matched, master_list)

    # --- Reorder: put the most job-relevant category first ---
    # Count how many extracted skills each category covers
    def _relevance_score(cat_skills):
        return sum(1 for s in cat_skills if s.lower() in extracted_flat)

    # Sort: highest job-match count first, but keep Programming Languages at top
    # and Soft Skills at bottom
    lang_entry = result.pop("Programming Languages", None)
    soft_entry = result.pop("Soft Skills", None)

    sorted_middle = sorted(result.items(), key=lambda x: _relevance_score(x[1]), reverse=True)

    final = {}
    if lang_entry:
        final["Programming Languages"] = lang_entry
    for cat, skills in sorted_middle:
        final[cat] = skills
    if soft_entry:
        final["Soft Skills"] = soft_entry

    return final


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
  "is_ai_focused": true,
  "summary": "A 2-3 sentence professional summary tailored to this job, highlighting the candidate's most relevant experience and skills. Bold-worthy keywords should be noted."
}}

Rules:
- Extract ALL technical skills, tools, methodologies, and soft skills from the job description — be thorough, include things like Git, Docker, CI/CD, Agile, specific cloud services, databases, testing tools, etc.
- Group them into logical categories
- matched_skills should include skills the candidate likely has based on their experience, INCLUDING transferable and related skills
- matching_score: PROJECTED match score after the resume is tailored. A software engineer applying for a similar role should score 0.75-0.95. Only score below 0.60 for a completely different domain.
- is_ai_focused: true ONLY if the job is primarily about AI/ML/LLM/data science. If AI is just mentioned or a small part, set false.
- summary should be compelling, ATS-friendly, and reference specific technologies from the job description
- Return ONLY valid JSON, no markdown fences"""

    response = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )

    result = _parse_json_response(response.content[0].text)

    is_ai_focused = result.pop("is_ai_focused", False)

    selected_skills = _select_skills_from_master(
        result["extracted_skills"], is_ai_focused
    )

    resp = AnalyzeJobResponse(**result)
    resp._selected_skills = selected_skills
    resp._is_ai_focused = is_ai_focused
    return resp


async def generate_resume_content(
    personal_info: PersonalInfo,
    experiences: List[Experience],
    education: List[Education],
    job_description: JobDescription,
    extracted_skills: Optional[Dict[str, List[str]]] = None,
    selected_skills: Optional[Dict[str, List[str]]] = None,
    is_ai_focused: bool = False,
) -> GenerateResumeResponse:
    # --- Dynamic bullet count for page 1 ---
    # With 10.5pt body, 1.08 line spacing, After 4pt: effective ~15pt per line
    # Page = 10" usable height = 720pt → ~48 body-equivalent lines
    # But headers are larger (28pt name, 16pt section headers, etc.)
    skill_lines = _estimate_skill_lines(selected_skills) if selected_skills else 6

    # Header block estimates in body-line equivalents:
    # name(3) + title(1.5) + contact(2) + profile_header(2) + profile_body(3) + skills_header(2) + skill_lines + work_exp_header(2) + company+period(2.5)
    header_lines = 3 + 1.5 + 2 + 2 + 3 + 2 + skill_lines + 2 + 2.5
    available_lines = 48 - header_lines
    # Each bullet ≈ 2 lines (25-30 words at 10.5pt wraps to ~2 lines)
    # Subtract 1 as safety margin for line spacing / After 4pt accumulation
    first_exp_bullets = max(5, min(10, int(available_lines // 2) - 1))

    # --- Bullet counts for remaining experiences (fill page 2) ---
    num_exp = len(experiences)
    if num_exp == 1:
        bullet_counts = [first_exp_bullets]
    elif num_exp == 2:
        bullet_counts = [first_exp_bullets, 10]
    elif num_exp == 3:
        bullet_counts = [first_exp_bullets, 8, 7]
    else:
        bullet_counts = [first_exp_bullets, 8, 7] + [6] * (num_exp - 3)

    experience_entries = []
    for i, exp in enumerate(experiences):
        experience_entries.append(
            f"Company {i+1}: {exp.role} at {exp.company_name} ({exp.start_date} - {exp.end_date}), {exp.location}\n"
            f"Description: {exp.description or 'N/A'}\n"
            f"Required bullets: EXACTLY {bullet_counts[i]}"
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
  "experiences": [
    {{
      "company_name": "{experiences[0].company_name}",
      "role": "{experiences[0].role}",
      "location": "{experiences[0].location}",
      "period": "{experiences[0].start_date} – {experiences[0].end_date}",
      "bullets": [
        {{
          "text": "Led the migration of legacy monolith services to microservices using Python and FastAPI, resolving performance bottlenecks and reducing API response times by 40% across 3 production environments.",
          "bold_keywords": ["Python", "FastAPI", "microservices"]
        }}
      ]
    }}
  ]
}}

CRITICAL RULES FOR BULLET POINTS — EACH BULLET MUST DESCRIBE REAL-WORLD HANDS-ON WORK:
1. Each bullet MUST be exactly 25-30 words (~2 lines on a resume)
2. Each bullet MUST describe a SPECIFIC, CONCRETE project or initiative — NOT a generic responsibility
3. Every bullet must read as if the candidate personally built, deployed, or led the work
4. Follow this exact pattern for EVERY bullet:
   [Action verb] + [specific system/project built or changed] + [using specific technologies] + [to solve a specific problem] + [with measurable result]
5. GOOD examples (real-world, hands-on, project-based):
   - "Led the migration of legacy .NET Framework 4.8 services to .NET 8 to resolve performance bottlenecks and reduce technical debt by 35%."
   - "Built a Kafka-based event streaming architecture using Java and Spring Boot to replace polling mechanisms, boosting real-time data throughput by 60%."
   - "Created Python-based ETL pipelines using Airflow and Pandas to replace slow SQL Server jobs, cutting nightly data sync duration from 4 hours to 45 minutes."
   - "Architected a RAG-based document retrieval system using LangChain and OpenAI embeddings, reducing manual research time by 70% for a team of 15 analysts."
6. BAD examples (too generic — DO NOT write bullets like these):
   - "Developed software applications using modern technologies and best practices to improve system performance."
   - "Worked on backend services and APIs to support business requirements."
7. Describe real-world engineering scenarios: migrations, performance optimizations, system redesigns, pipeline builds, infrastructure automation, API integrations, ML model deployments
8. Include operational context: production environments, team sizes, user scale, traffic volume
9. Each bullet must name SPECIFIC technologies from the job description
10. Include realistic metrics (%, time saved, scale, throughput, cost reduction)
11. bold_keywords should list the technologies/tools in each bullet that match the job description
12. Vary action verbs: Led, Built, Architected, Implemented, Designed, Created, Refactored, Automated, Deployed, Integrated, Migrated, Optimized
13. Each bullet must describe a DISTINCT project — no two bullets should describe the same type of work
14. BULLET COUNTS ARE MANDATORY:
{chr(10).join(f'    - {experiences[i].company_name}: EXACTLY {bullet_counts[i]} bullets' for i in range(num_exp))}
15. Even for older companies, weave in modern tech context where realistic (e.g. migrating to React, introducing Node.js, adding TypeScript)

DO NOT include a "skills" field — skills are handled separately.

Return ONLY valid JSON, no markdown fences."""

    response = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}],
    )

    result = _parse_json_response(response.content[0].text)

    final_skills = selected_skills if selected_skills else {}

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
        skills=final_skills,
        experiences=exp_outputs,
        education=education,
        personal_info=personal_info,
        filename="",
    )
