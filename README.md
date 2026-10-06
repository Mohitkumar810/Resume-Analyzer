# AI Resume Analyzer & Job Matcher

A no-login web app that compares one PDF or DOCX resume with a pasted job description. It uses document text extraction, a small editable skill dictionary, TF-IDF, and cosine similarity to provide an explainable match score and practical feedback.

## Features

- Extracts selectable text from PDF and DOCX files, including DOCX tables.
- Shows matched skills, skills mentioned in the job description but not detected in the resume, and job-description keywords.
- Calculates the score from text similarity (60%) and detected skill coverage (40%). If no dictionary skills are found in the job description, it uses text similarity alone.
- Does not require an AI API key, account, or database.
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

- Uploads must be PDF or DOCX and are limited to 5 MB. Job descriptions must contain 30–20,000 characters.
- Scanned/image-only PDFs are not OCR processed. Use a text-based PDF or DOCX.
- Skill recognition depends on the curated dictionary in `backend/app/analyzer.py`; unlisted skills may not appear in the breakdown.
- TF-IDF and skill coverage are simple matching signals, not a measure of candidate quality or a hiring recommendation.
- No resume contents or analysis results are persisted. Uploaded bytes are read in memory and the upload handle is closed after parsing.
