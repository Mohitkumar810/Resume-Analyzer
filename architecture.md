# Architecture

## Overview

The application is a single FastAPI service that serves a static browser UI and a multipart analysis endpoint. Analysis runs locally in the backend process using document parsers and scikit-learn; there is no database, external AI service, or persisted upload storage.

```text
Browser
  ├─ GET / and /assets/*
  └─ POST /api/analyze (multipart form)
       ├─ Validate resume and job-description inputs
       ├─ Extract document text (pypdf / python-docx / UTF-8 TXT)
       ├─ Build resume profile (backend/app/analyzer.py)
       ├─ Analyze each job independently
       ├─ Rank results by estimated match score
       └─ Return validated JSON (Pydantic response models)
```

## Components

### Frontend: `frontend/`

- `index.html` defines the accessible form, repeatable job-description fields, optional multi-file upload, live results region, and file/type guidance.
- `app.js` validates the number of descriptions, creates multipart form data, omits the optional `job_files` field when no files are selected, submits the request, and renders results using DOM text nodes.
- `styles.css` contains the small visual layer over Bootstrap 5.3.3, loaded from the jsDelivr CDN.

### API and response models: `backend/app/main.py`

- Serves `frontend/index.html` at `/` and static frontend files at `/assets`.
- Exposes `/api/health` and `POST /api/analyze`.
- Validates the resume extension, upload size, description count, and description lengths.
- Parses uploaded job-description files and closes uploaded file handles in a `finally` block.
- Calls the analyzer, sorts recommendations by descending score (preserving input order for ties), and validates the output with Pydantic models.
- Returns explicit HTTP errors for unsupported file types, unreadable documents, empty input, and limit violations.

### Document parsing: `backend/app/document_parser.py`

- Reads PDF bytes with `pypdf` and extracts page text.
- Reads DOCX bytes with `python-docx`, including paragraphs and table-cell text.
- Cleans blank lines and raises `DocumentParsingError` for unsupported, unreadable, encrypted, or textless documents.
- Does not OCR scanned PDFs.

### Analysis: `backend/app/analyzer.py`

- Maintains skill aliases, skill categories, section-heading aliases, and preferred-qualification markers.
- Extracts a likely name and section contents; detects missing/weak sections and recognized skills.
- Uses regex and labeled-section heuristics for skill, qualification, and experience requirement extraction.
- Uses scikit-learn TF-IDF and cosine similarity for text similarity and keyword extraction.
- Builds one result per description, including score components, detected matches/gaps, learning steps, and improvement suggestions.
- Performs no network requests or durable writes.

## API flow and payload

`POST /api/analyze` accepts multipart form data:

- Required `resume`: one PDF or DOCX.
- Optional `job_description`: one legacy/single pasted description.
- Optional repeated `job_descriptions`: pasted descriptions from the current UI.
- Optional repeated `job_files`: PDF, DOCX, or TXT uploads.

At least one non-empty description must be present across the text and file fields. The response contains the top recommendation's `JobAnalysis` fields at the top level, a `resume_profile`, input-order `job_analyses`, and score-ranked `recommendations`. See the `AnalysisResponse`, `JobAnalysis`, `ResumeProfile`, and `ScoreBreakdown` models in `backend/app/main.py` for the authoritative schema.

## Match calculation

The overall estimate is a weighted sum of rounded component percentages:

- Skills: 30%
- Education: 15%
- Experience: 20%
- Projects: 15%
- Keywords: 20%

The skills component uses required-skill coverage when dictionary skills are found in the job description; otherwise it falls back to text similarity. Education and projects use section-to-description text similarity. Experience uses an estimated date-range ratio if the resume and job provide recognizable year ranges/requirements; otherwise it uses section text similarity. Keywords measure detected overlap with the job's extracted top TF-IDF terms. These are explainable heuristic signals, not a calibrated predictive model.

## Privacy and security boundaries

- Upload bytes are read in memory with a 5 MB per-file read limit; no application code stores resume contents or analysis history.
- Do not log raw resumes, job descriptions, contact details, or extracted profile text.
- Preserve explicit input limits and close uploaded handles on all request paths.
- Treat extracted document content as untrusted plain text; never render it as HTML or execute it.
- HTTPS, deployment-level request timeouts, reverse-proxy body limits, and CDN availability are deployment responsibilities.

## Local development and checks

From the repository root:

```powershell
python -m uvicorn backend.app.main:app --reload
python -m pytest backend/tests -q
node --check frontend/app.js
```

Dependencies are declared in `requirements.txt` and `requirements-dev.txt`.
