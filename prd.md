# Product Requirements Document

## Product

**Resume Analyzer & Job Matcher** is a private, no-login web app that helps job seekers compare a resume with one or more job descriptions. It extracts readable document text, surfaces relevant evidence and gaps, and provides explainable, heuristic feedback.

## Problem

Applicants often have to compare their resume with each job posting manually. They need a quick way to identify relevant skills, notice missing evidence, prioritize roles, and make specific, truthful improvements to their resume.

## Goals

- Analyze a PDF or DOCX resume and identify likely resume sections and recognized skills.
- Accept pasted job descriptions and uploaded PDF, DOCX, or TXT descriptions.
- Compare resume evidence with required and preferred skills and qualifications.
- Explain the estimated match with separate skills, education, experience, projects, and keyword scores.
- Identify missing required skills and suggest a practical learning starting point.
- Recommend a specific resume improvement rather than giving only generic advice.
- Rank multiple job descriptions by estimated match.
- Process documents without accounts, an AI API key, a database, or persistent resume storage.

## Users

Job seekers preparing or prioritizing applications. The product is an informational self-assessment aid, not a recruiting, screening, or hiring system.

## User experience

1. The user uploads one PDF or DOCX resume.
2. The user pastes one or more job descriptions, uploads one or more job-description files, or combines pasted and uploaded descriptions.
3. The user starts analysis and sees actionable validation errors if a file or description is unsupported or outside documented limits.
4. The result shows ranked jobs, a breakdown for the top-ranked job, resume extraction, skill matches and gaps, qualifications, and improvement suggestions.
5. The user checks extracted details against their documents and includes only accurate claims in any revised resume.

## Functional requirements

### Resume analysis

- Extract selectable text from PDF and DOCX. DOCX paragraphs and table cells are supported; scanned PDFs are not OCR processed.
- Return a likely name; education, experience, projects, and certifications text; recognized skills and categories; and sections classified as missing or weak.
- Distinguish recognized technical skills from recognized soft skills.

### Job-description analysis and matching

- Support pasted descriptions and PDF, DOCX, and UTF-8 TXT files.
- Recognize skills in the maintained skill dictionary and group them by category.
- Separate preferred skills or qualifications where the posting labels a preferred section; extract explicit experience-duration requirements and required qualifications where recognizable.
- Return matched, missing, and preferred skills.
- Compute an overall estimated score and show its component scores: Skills, Education, Experience, Projects, and Keywords.
- Return suggested learning steps for missing required skills.
- Rank up to 10 job descriptions; the top-ranked job supplies the headline match and detailed view.

### Resume improvement

- Flag missing or weak sections and suggest how to strengthen them.
- Offer concrete, editable guidance for turning vague statements into specific, evidence-based accomplishments. Do not invent candidate experience, numbers, credentials, or skills.

## Constraints and limits

- Resume and job-description uploads: at most 5 MB each.
- Each job description: 30 to 20,000 characters after extraction or trimming.
- Maximum of 10 descriptions per analysis request.
- Resume file types: PDF and DOCX. Job-description file types: PDF, DOCX, and TXT.
- No authentication, database, analysis history, OCR, external AI provider, or claim that a percentage predicts hiring outcomes.

## Success criteria

- Supported resumes and job descriptions are accepted; invalid types, unreadable documents, and size or text-limit violations return explicit errors.
- A user can submit pasted job text without selecting an optional job-description file.
- The response includes extracted resume details, all five score dimensions, skill gaps, improvement suggestions, and ranked recommendations.
- Ranking is descending by match score and remains stable for ties.
- The backend regression suite passes and frontend JavaScript parses successfully.

## Known limitations

Extraction and classification rely on document text layout, simple section-heading heuristics, regular expressions, a curated skill dictionary, and TF-IDF. A section or name can be missed, an unlabeled preferred qualification can be misclassified, and experience or relevance scores are approximate. The product must communicate these limitations and avoid presenting its scores as objective assessments.
