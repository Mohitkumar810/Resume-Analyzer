from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.app.analyzer import analyze_match
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
    text_similarity: int
    skill_coverage: int | None
    scoring_note: str


class AnalysisResponse(BaseModel):
    match_score: int
    score_breakdown: ScoreBreakdown
    matched_skills: list[str]
    missing_skills: list[str]
    resume_skills: list[str]
    job_keywords: list[str]
    suggestions: list[str]


@app.get("/", include_in_schema=False)
async def homepage() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/api/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
) -> AnalysisResponse:
    try:
        filename = resume.filename or ""
        if Path(filename).suffix.lower() not in {".pdf", ".docx"}:
            raise HTTPException(status_code=415, detail="Upload a PDF or DOCX resume.")

        content = await resume.read(MAX_RESUME_BYTES + 1)
        if len(content) > MAX_RESUME_BYTES:
            raise HTTPException(status_code=413, detail="Resume file must be 5 MB or smaller.")

        cleaned_job_description = job_description.strip()
        if len(cleaned_job_description) < MIN_JOB_DESCRIPTION_LENGTH:
            raise HTTPException(
                status_code=422,
                detail=f"Job description must be at least {MIN_JOB_DESCRIPTION_LENGTH} characters.",
            )
        if len(cleaned_job_description) > MAX_JOB_DESCRIPTION_LENGTH:
            raise HTTPException(
                status_code=422,
                detail=f"Job description must be {MAX_JOB_DESCRIPTION_LENGTH} characters or fewer.",
            )

        resume_text = extract_document_text(filename, content)
        if len(resume_text) < 40:
            raise HTTPException(
                status_code=422,
                detail="The resume contains too little readable text to analyze.",
            )

        result = analyze_match(resume_text, cleaned_job_description)
        return AnalysisResponse(**result)
    except DocumentParsingError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    finally:
        await resume.close()
