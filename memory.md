# Project Memory

## Stable project facts

- This repository contains a Python FastAPI service and a static JavaScript/HTML/CSS frontend.
- Backend entry point: `backend.app.main:app`.
- Frontend assets: `frontend/`; served at `/` and `/assets`.
- Analyzer and its skill dictionary/scoring logic: `backend/app/analyzer.py`.
- PDF/DOCX extraction: `backend/app/document_parser.py`.
- Backend tests: `backend/tests/`.
- Runtime dependencies are in `requirements.txt`; test dependencies are in `requirements-dev.txt`.
- The app does not require an account, database, AI key, or external AI provider.

## Current product behavior

- One PDF/DOCX resume is compared with 1–10 job descriptions.
- Job descriptions can be pasted and/or uploaded as PDF, DOCX, or TXT.
- Each file is limited to 5 MB; each description must be 30–20,000 characters.
- The response includes a resume profile, per-input analyses, and stably ranked recommendations.
- The top recommendation's analysis is also returned at the response top level.
- The match estimate weights Skills 30%, Education 15%, Experience 20%, Projects 15%, and Keywords 20%.
- Resume files are read in memory. Application code does not store uploaded documents or analysis results.

## Important implementation details

- The browser must remove `job_files` from `FormData` when no file is selected. Sending an empty file part can make FastAPI reject the request before the endpoint runs.
- Skill extraction is dictionary/alias based. Preferred-skill separation depends on labeled preferred sections/markers; section extraction depends on headings.
- The frontend renders extracted and user-supplied content via text nodes. Keep it that way.
- Score percentages are heuristics, not a calibrated model, and must not be presented as hiring decisions.
- `README.md` is the local setup and user-facing limitations guide; see `architecture.md`, `rules.md`, and `design.md` for implementation context.

## Development checks

```powershell
python -m uvicorn backend.app.main:app --reload
python -m pytest backend/tests -q
node --check frontend/app.js
git diff --check
```

## Known caveats

- Scanned/image-only PDF resumes and job descriptions are not OCR processed.
- Name and section extraction can be incorrect for nonstandard layouts.
- Skill recognition is limited to the curated dictionary and aliases.
- Qualification labeling and experience ranges are extracted with lightweight text heuristics.
- Bootstrap is loaded from a public CDN.
- Keep test fixtures synthetic; never commit real resumes or personal job-application data.
