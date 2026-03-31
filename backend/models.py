from pydantic import BaseModel
from typing import Dict, List, Optional


class PersonalInfo(BaseModel):
    full_name: str
    title: str  # e.g. "Senior Software Engineer"
    email: str
    phone: str
    location: str
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    github_url: Optional[str] = None


class Experience(BaseModel):
    company_name: str
    role: str
    location: str
    start_date: str  # e.g. "01/2021"
    end_date: str  # e.g. "Present" or "06/2025"
    company_url: Optional[str] = None
    description: Optional[str] = None  # brief description of what user did


class Education(BaseModel):
    institution: str
    degree: str  # e.g. "Bachelor's Degree in Computer Science"
    location: str
    start_date: str
    end_date: str
    description: Optional[str] = None


class JobDescription(BaseModel):
    company_name: str
    company_url: Optional[str] = None
    job_title: str
    description: str  # full job description text


class AnalyzeJobRequest(BaseModel):
    job_description: JobDescription
    experiences: List[Experience]


class AnalyzeJobResponse(BaseModel):
    extracted_skills: Dict[str, List[str]]  # category -> skills list
    matched_skills: List[str]
    matching_score: float
    summary: str


class GenerateResumeRequest(BaseModel):
    personal_info: PersonalInfo
    experiences: List[Experience]
    education: List[Education]
    job_description: JobDescription
    extracted_skills: Optional[Dict[str, List[str]]] = None


class BulletPoint(BaseModel):
    text: str
    bold_keywords: List[str] = []


class ExperienceOutput(BaseModel):
    company_name: str
    role: str
    location: str
    period: str
    bullets: List[BulletPoint]


class GenerateResumeResponse(BaseModel):
    summary: str
    skills: Dict[str, List[str]]
    experiences: List[ExperienceOutput]
    education: List[Education]
    personal_info: PersonalInfo
    filename: str  # generated file name
