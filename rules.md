# Project Rules

These are project-specific implementation and product rules. Follow the repository's existing Python, JavaScript, HTML, and CSS patterns.

## Product behavior

1. Describe analysis results as estimates from local heuristics, not AI-generated judgments, objective candidate quality measures, or hiring recommendations.
2. Never fabricate a person's qualifications, experience, metrics, education, certifications, or skill proficiency. Suggestions must be conditional on truthful supporting evidence.
3. Treat detected content as uncertain: tell users to review extracted content, particularly when using unusual resume layouts.
4. Preserve paste-only job-description analysis. Job-description uploads are optional.
5. Support the documented limit of 10 total job descriptions, whether pasted, uploaded, or combined.
6. Keep the top-level analysis consistent with the highest-ranked recommendation; keep `job_analyses` in input order and rank `recommendations` by score, stably breaking ties by input order.

## Input and privacy

1. Accept resumes only as PDF or DOCX and job-description uploads only as PDF, DOCX, or UTF-8 TXT.
2. Keep the 5 MB per-file, 30-character minimum, and 20,000-character maximum limits consistent across API validation, frontend hints/validation, README, and tests.
3. Report malformed or unsupported uploads explicitly with the repository's HTTP error conventions. Do not turn parse failures into success-shaped empty results.
4. Keep uploaded content in memory. Do not add resume persistence, analytics containing document text, or raw-content logging without an explicit product/privacy decision.
5. Close every `UploadFile`, including files on error paths.
6. Render user- or document-supplied text as text, not interpolated HTML.

## Analysis and API

1. Keep `backend/app/main.py` response models aligned with analyzer output and frontend usage.
2. Keep skill aliases and skill categories defined centrally in `backend/app/analyzer.py`; avoid duplicating skill-matching logic in the API or browser.
3. Keep skill matching case-insensitive and boundary-aware to avoid incidental substring matches.
4. Make scoring behavior and limitations explainable; update `architecture.md` and tests when changing score weights or component definitions.
5. Use explicit types and narrow error handling. Avoid broad exception catches, silent fallbacks, and speculative values.

## Frontend and accessibility

1. Use semantic labels, buttons, live status/result regions, and progress-bar accessibility attributes.
2. Preserve keyboard-operable repeatable job fields and clear loading/error states.
3. Keep the optional job file out of `FormData` when no file is selected; browsers may otherwise submit an empty file part that FastAPI cannot parse as an `UploadFile`.
4. Keep dynamic text inserted via `textContent`/text nodes, and keep filename accept filters aligned with backend-supported file types.
5. Follow the existing Bootstrap-based styles and responsive layout rather than adding a second UI framework.

## Validation and changes

1. Add or update focused backend tests when changing extraction, validation, scores, ranking, or response structure.
2. Run `python -m pytest backend/tests -q`, `node --check frontend/app.js`, and `git diff --check` for relevant changes.
3. Update user-facing docs when supported inputs, limits, privacy behavior, score weights, or known limitations change.
4. Do not commit temporary resumes, extracted personal information, secrets, virtual environments, or test artifacts.
