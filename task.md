# Project Task Backlog

This checklist records the current product scope and follow-up work. “Done” describes functionality present in the repository; it is not a claim that future validation or deployment work is complete.

## Implemented scope

- [x] Upload and parse PDF/DOCX resumes; enforce file size and reject unsupported or unreadable files.
- [x] Extract likely name, education, experience, projects, certifications, and recognized skills.
- [x] Identify skill categories and recognized technical and soft skills.
- [x] Flag missing or weak resume sections.
- [x] Paste one or more job descriptions and upload PDF, DOCX, or TXT descriptions.
- [x] Extract recognized required/preferred skills, labeled qualifications, and experience-duration requirements.
- [x] Calculate overall match estimates and Skills, Education, Experience, Projects, and Keywords breakdowns.
- [x] Show skill gaps, a starting learning roadmap, and specific, evidence-conscious resume advice.
- [x] Rank up to 10 jobs and show the highest-ranked job's detailed analysis.
- [x] Keep the optional job-file field out of the browser request when no file is selected.
- [x] Keep uploads and analyses in memory without application-level persistence.
- [x] Cover analyzer and API behavior with backend tests.

## Recommended follow-up

- [ ] Improve section extraction against representative multi-column, table-heavy, and varied-format resumes; add sanitized fixture documents and expected extraction tests.
- [ ] Expand skill aliases and qualification parsing from user-reviewed examples; verify word-boundary behavior for abbreviations and punctuation-heavy names.
- [ ] Review scoring with a labeled, consented evaluation set before treating component weights or recommendations as useful beyond exploratory guidance.
- [ ] Improve experience-duration matching to handle open-ended ranges, months, overlapping roles, and requirements such as “3+ years.”
- [ ] Add explicit frontend regression coverage for no-file form submission, combined input counting, error rendering, and ranked results.
- [ ] Add operational deployment limits, request timeouts, HTTPS, and privacy-safe observability appropriate to the hosting platform.
- [ ] Decide whether to pin or self-host Bootstrap for offline use and stricter supply-chain control.
- [ ] Collect user feedback on suggestion clarity and extraction errors without retaining uploaded resume content.

## Release checklist

- [ ] Run `python -m pytest backend/tests -q`.
- [ ] Run `node --check frontend/app.js`.
- [ ] Verify upload limits, file types, total-job limit, paste-only flow, and error messages in a browser.
- [ ] Confirm privacy copy matches actual hosting/logging behavior.
- [ ] Review the known limitations and scoring explanation in `README.md`.
