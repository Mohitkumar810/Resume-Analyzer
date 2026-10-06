from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.app.analyzer import analyze_match, analyze_resume as extract_resume_profile
from backend.app.document_parser import DocumentParsingError, extract_document_text


MAX_RESUME_BYTES = 5 * 1024 * 1024
MAX_JOB_DESCRIPTION_LENGTH = 20_000
MIN_JOB_DESCRIPTION_LENGTH = 30
PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DIR = PROJECT_ROOT / "frontend"

app = FastAPI(
    title="AI Resume Analyzer & Job Matcher",
    description="Compare a resume with a job description using explainable NLP techniques.",
    version="1.0.0",
)
app.mount("/assets", StaticFiles(directory=FRONTEND_DIR), name="assets")


class ScoreBreakdown(BaseModel):
    skills: int
    education: int
    experience: int
    projects: int
    keywords: int
    text_similarity: int
    skill_coverage: int | None
    scoring_note: str


class ResumeProfile(BaseModel):
    name: str | None
    education: str
    experience: str
    projects: str
    certifications: str
    skills: list[str]
    technical_skills: list[str]
    soft_skills: list[str]
    skills_by_category: dict[str, list[str]]
    missing_weak_sections: list[dict[str, str]]


class JobAnalysis(BaseModel):
    job_title: str
    match_score: int
    score_breakdown: ScoreBreakdown
    matched_skills: list[str]
    missing_skills: list[str]
    preferred_skills: list[str]
    matched_preferred_skills: list[str]
    missing_preferred_skills: list[str]
    required_skills: list[str]
    resume_skills: list[str]
    job_keywords: list[str]
    skill_categories: dict[str, list[str]]
    experience_requirements: list[str]
    required_qualifications: list[str]
    preferred_qualifications: list[str]
    learning_roadmap: list[dict[str, str]]
    suggestions: list[str]


class AnalysisResponse(JobAnalysis):
    resume_profile: ResumeProfile
    job_analyses: list[JobAnalysis]
    recommendations: list[JobAnalysis]


@app.get("/", include_in_schema=False)
async def homepage() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/api/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str | None = Form(None),
    job_descriptions: list[str] | None = Form(None),
    job_files: list[UploadFile] | None = File(None),
) -> AnalysisResponse:
    uploads = job_files or []
    try:
        filename = resume.filename or ""
        if Path(filename).suffix.lower() not in {".pdf", ".docx"}:
            raise HTTPException(status_code=415, detail="Upload a PDF or DOCX resume.")

        content = await resume.read(MAX_RESUME_BYTES + 1)
        if len(content) > MAX_RESUME_BYTES:
            raise HTTPException(status_code=413, detail="Resume file must be 5 MB or smaller.")

        resume_text = extract_document_text(filename, content)
        if len(resume_text) < 40:
            raise HTTPException(
                status_code=422,
                detail="The resume contains too little readable text to analyze.",
            )

        descriptions = [text.strip() for text in (job_descriptions or []) if text.strip()]
        if job_description and job_description.strip():
            descriptions.insert(0, job_description.strip())
        for job_file in uploads:
            job_filename = job_file.filename or ""
            extension = Path(job_filename).suffix.lower()
            job_content = await job_file.read(MAX_RESUME_BYTES + 1)
            if len(job_content) > MAX_RESUME_BYTES:
                raise HTTPException(status_code=413, detail="Job description files must be 5 MB or smaller.")
            if extension in {".pdf", ".docx"}:
                description_text = extract_document_text(job_filename, job_content)
            elif extension == ".txt":
                try:
                    description_text = job_content.decode("utf-8-sig").strip()
                except UnicodeDecodeError as exc:
                    raise HTTPException(status_code=422, detail="Job description text files must use UTF-8 encoding.") from exc
            else:
                raise HTTPException(status_code=415, detail="Upload job descriptions as PDF, DOCX, or TXT files.")
            descriptions.append(description_text)

        if not descriptions:
            raise HTTPException(status_code=422, detail="Paste or upload at least one job description.")
        if len(descriptions) > 10:
            raise HTTPException(status_code=422, detail="Analyze up to 10 job descriptions at a time.")
        for description in descriptions:
            if len(description) < MIN_JOB_DESCRIPTION_LENGTH:
                raise HTTPException(
                    status_code=422,
                    detail=f"Each job description must be at least {MIN_JOB_DESCRIPTION_LENGTH} characters.",
                )
            if len(description) > MAX_JOB_DESCRIPTION_LENGTH:
                raise HTTPException(
                    status_code=422,
                    detail=f"Each job description must be {MAX_JOB_DESCRIPTION_LENGTH} characters or fewer.",
                )

        profile = extract_resume_profile(resume_text)
        analyses = [analyze_match(resume_text, description, profile) for description in descriptions]
        ranked = sorted(enumerate(analyses), key=lambda item: (-item[1]["match_score"], item[0]))
        recommendations = [analysis for _, analysis in ranked]
        return AnalysisResponse(
            **recommendations[0],
            resume_profile=profile,
            job_analyses=analyses,
            recommendations=recommendations,
        )
    except DocumentParsingError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    finally:
        await resume.close()
        for job_file in uploads:
            await job_file.close()
