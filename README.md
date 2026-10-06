# AI Resume Analyzer & Job Matcher

A no-login web app that analyzes a PDF or DOCX resume against one or more job descriptions. It extracts resume sections and skills, identifies skill gaps and preferred qualifications, estimates a transparent match breakdown, suggests concrete resume edits, and ranks multiple roles.

## Features

- Extracts selectable text from PDF and DOCX resumes, including DOCX tables; job descriptions can be pasted or uploaded as PDF, DOCX, or TXT.
- Detects a likely name, education, experience, projects, certifications, technical skills, soft skills, and missing or weak resume sections.
- Categorizes skills (programming, databases, cloud, frameworks, DevOps and tools, data and analytics, ways of working, and soft skills), and separates preferred skills and qualifications from required ones where they are labeled in the job description.
- Reports skills, education, experience, projects, and keyword scores, plus matched skills, missing skills, experience requirements, and a learning roadmap.
- Gives specific, evidence-conscious resume suggestions, including an example template for rewriting vague project or experience bullets.
- Ranks up to 10 job descriptions by estimated resume match. Add several pasted descriptions or upload multiple job-description files.
- Calculates the overall estimate using skills (30%), education (15%), experience (20%), projects (15%), and keywords (20%). The skills score falls back to text similarity when no dictionary skills are detected.
- Does not require an AI API key, account, or database. The analysis uses local heuristics, a curated skill dictionary, TF-IDF, and cosine similarity; it is not an AI model or hiring decision.
- Processes uploads in memory and does not save resumes or analysis history.

## Run locally

Requires Python 3.10 or newer.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m uvicorn backend.app.main:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000). Interactive API documentation is available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Run tests

```powershell
python -m pytest backend/tests -q
```

## Limits and privacy

- Resume and job-description files are limited to 5 MB each. Each job description must contain 30–20,000 characters; analyze up to 10 jobs at a time.
- Scanned/image-only PDFs are not OCR processed. Use a text-based PDF or DOCX.
- Section, name, skill, and qualification recognition depends on text layout and the curated dictionary in `backend/app/analyzer.py`; unlisted skills or unlabeled qualifications may not appear in the breakdown.
- Match percentages and experience estimates are approximate text-based signals, not a measure of candidate quality or a hiring recommendation. Verify extracted details and only add truthful resume claims.
- No resume contents or analysis results are persisted. Uploaded bytes are read in memory and the upload handle is closed after parsing.
