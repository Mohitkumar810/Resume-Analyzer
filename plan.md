# Resume Analyzer & Job Matcher — Product Plan

> **A clearer next step for every application.** Help job seekers compare their experience with real job requirements, understand what the comparison does—and does not—say, and decide what to improve next.

## 1. Executive overview

The Resume Analyzer & Job Matcher is a private, no-login web app for comparing one resume with one or more job descriptions. It extracts readable text, identifies likely resume sections and recognized skills, highlights areas of overlap and gaps, and presents an explainable estimate of how closely the documents align.

The product is designed to make a tedious manual review easier—not to make a decision on someone's behalf. It uses local, rule-based analysis and text similarity rather than an external AI service. Its scores are directional signals, not predictions of hiring success or measures of a person's worth.

The plan is to strengthen the reliability and usefulness of the existing experience before expanding its scope. First make extraction and explanations more dependable; then validate the analysis and improve the workflow; finally prepare deployment and privacy practices for the environment where the app will run.

### At a glance

| Area | Direction |
|---|---|
| **For** | Job seekers preparing applications or deciding which roles to prioritize |
| **Main benefit** | Turn a resume and job posting into a useful, inspectable comparison |
| **Current approach** | Local document parsing, curated skill matching, heuristics, and TF-IDF text similarity |
| **Product promise** | Explain what was detected, show where it came from, and offer practical next steps |
| **Not the promise** | Predicting hiring outcomes, ranking candidate quality, or replacing human judgment |
| **Near-term priority** | Improve extraction quality and validate the analysis before adding broader features |

## 2. The problem we are solving

Before applying, a job seeker has to answer several practical questions:

- Which parts of my experience are relevant to this specific role?
- Which required skills can I support with evidence in my resume?
- What might be missing—or simply hard for a reader to find?
- If I am applying to several roles, where should I focus first?
- How can I make a resume bullet clearer without exaggerating what I did?

Answering these questions manually for every posting takes time, and generic resume advice does not always help with the next concrete edit. This product brings the comparison into one place and gives users a structured starting point.

The analysis is only as good as the text it can read and the patterns it recognizes. The plan therefore treats accuracy, plain-language explanations, and honest limitations as core product work—not fine print.

## 3. Product vision and principles

### Vision

Make it easier for people to understand how their existing experience relates to a role, find questions worth reviewing, and prepare a more relevant and truthful application.

### Principles that guide decisions

1. **Useful, not authoritative.** Present match values as estimates and never as hiring recommendations.
2. **Evidence before advice.** Show detected overlap and gaps so users can inspect the basis of a suggestion.
3. **Truthful improvement.** Help users express real experience more clearly; never invent skills, metrics, credentials, or accomplishments.
4. **Privacy by default.** Keep analysis local to the service request, avoid accounts and history, and do not retain uploaded documents in application storage.
5. **Clarity over cleverness.** Prefer understandable labels, visible limits, and specific next steps over opaque scores or vague AI language.
6. **Accessible and responsive.** Make the workflow usable with keyboard, assistive technology, and small screens.
7. **Incremental confidence.** Improve and validate what the product already does before promising broader capabilities.

## 4. Who the product serves

### Primary user

A job seeker who has a resume and one or more job descriptions, and wants help reviewing alignment before deciding how to tailor an application.

### User needs

- A straightforward way to provide a resume and job descriptions.
- A quick summary of relevant evidence and possible gaps.
- A way to compare several roles without repeating the whole process manually.
- Suggestions that can be checked against their actual experience.
- Confidence that the app is not silently storing their resume or making a hiring decision.

### Out of scope

The product is not intended to be a hiring, recruiting, screening, or candidate-ranking system. It does not verify a person's claims, make career decisions, guarantee application success, or replace careful review of the original documents.

## 5. What the product does today

The current experience supports the core comparison workflow:

### Resume input and profile

- Accepts one PDF or DOCX resume and extracts selectable text.
- Reads DOCX paragraph and table-cell text.
- Identifies likely resume sections, such as education, experience, projects, and certifications.
- Detects skills from a maintained dictionary, groups them into categories, and flags sections that appear missing or weak.

### Job-description input

- Accepts pasted descriptions and uploaded PDF, DOCX, or UTF-8 TXT files.
- Supports up to 10 total job descriptions in one analysis.
- Enforces the documented 5 MB per-file upload limit and the 30–20,000 character range for each description.
- Recognizes listed skills and qualifications where the wording and section labels make them detectable.

### Comparison and guidance

- Estimates an overall match and reports five components: Skills, Education, Experience, Projects, and Keywords.
- Shows detected matches, missing skills, preferred skills where recognized, and job recommendations ranked by estimated match.
- Provides a starting learning roadmap for missing required skills and specific resume-improvement suggestions.
- Keeps the detailed analysis focused on the highest-ranked job while retaining the individual analyses and ranked recommendations.

### Privacy and implementation

- Runs without a user account, database, or external AI API key.
- Processes uploaded content in memory and does not store resume or analysis history in application storage.
- Renders document-derived content as text rather than treating it as HTML.

### Important limits to communicate

- Scanned or image-only PDFs are not OCR processed.
- Section, name, skill, and qualification detection depend on text layout and heuristic rules.
- The skill dictionary may not include every relevant term.
- Preferred requirements may be missed if a posting does not label them clearly.
- Experience and match estimates are approximate text-based signals, not calibrated predictions.

## 6. The user journey we want to make effortless

1. **Start with a clear promise.** The page explains what the comparison can help with, what files are accepted, and what the estimate means.
2. **Add a resume.** The user selects a PDF or DOCX and sees the file-size and scanned-document guidance before analysis.
3. **Add one or more roles.** The user pastes job descriptions, uploads supported job-description files, or combines both.
4. **Check the inputs.** Clear validation explains unsupported files, unreadable text, empty descriptions, or limits that have been exceeded.
5. **Run the comparison.** The interface shows an active loading state and prevents accidental repeat submissions.
6. **Review the ranked roles.** The user can see which posting appears to align more closely according to the estimate.
7. **Inspect the evidence.** The breakdown, detected skills, gaps, qualifications, and extracted resume profile make the result easier to question and verify.
8. **Choose a next step.** The user can investigate a gap, improve a relevant resume section, or prioritize a role.
9. **Keep ownership of the decision.** The user checks all extracted details and only uses suggestions supported by truthful experience.

The experience should never make a percentage the only meaningful result. Explanations, evidence, and limitations should remain easy to find alongside the score.

## 7. Product roadmap

The roadmap prioritizes confidence and trust before breadth. Each phase should produce a useful outcome and a way to check whether that outcome was achieved.

### Phase 1 — Make document understanding more dependable

**Outcome:** Users can better trust that the text and sections shown in the result reflect the documents they provided.

**Work**

- Build a representative, privacy-safe set of resume fixtures covering varied headings, multi-column layouts, tables, and common formatting patterns.
- Compare extraction results against expected sections and text; add focused regression tests for failures found.
- Improve section extraction where the fixtures demonstrate recurring errors.
- Expand skill aliases and qualification parsing from reviewed examples, including abbreviations and punctuation-heavy names.
- Improve experience-duration parsing for cases such as “3+ years,” open-ended ranges, months, and overlapping roles.
- Make uncertain or unavailable extraction especially clear in the result rather than implying completeness.

**How we will know it helped**

- New representative documents produce the expected extracted sections in regression tests.
- Known extraction and parsing limitations are recorded with examples and remain visible in user-facing guidance.
- Changes to skill and qualification detection reduce demonstrated misses without introducing obvious substring false positives.

### Phase 2 — Make the comparison more useful and explainable

**Outcome:** Users can tell why a role received its estimate and can turn the result into a practical review.

**Work**

- Assemble a labeled, consented evaluation set before changing score weights or describing scores as more reliable.
- Review the five score components against that set and document what each component measures and where it is weak.
- Check that ranked recommendations remain in descending order and ties preserve input order.
- Add frontend regression coverage for paste-only submission, combined pasted/uploaded job counting, error states, loading behavior, and ranked results.
- Collect feedback on clarity and extraction errors without retaining resume contents.
- Refine suggestion wording based on whether users can identify a truthful, concrete next action.

**How we will know it helped**

- Score and ranking behavior is covered by tests and explained consistently across the interface and documentation.
- Users can distinguish detected evidence from missing or uncertain evidence.
- Feedback collection does not require storing uploaded documents or analysis text.

### Phase 3 — Prepare for responsible deployment

**Outcome:** The deployed service has operational controls that match the product's privacy promises and input limits.

**Work**

- Define hosting-specific upload/body limits, request timeouts, and HTTPS requirements.
- Review platform and proxy logging to ensure raw resumes, job descriptions, contact details, and extracted profile text are not recorded.
- Confirm that privacy copy describes the actual deployment—not just local application behavior.
- Decide whether to pin or self-host Bootstrap for offline availability and stricter supply-chain control.
- Document deployment configuration and operational checks for the chosen hosting environment.

**How we will know it helped**

- Deployment limits align with API limits and return understandable errors.
- A privacy review confirms that application and hosting logs do not expose document contents.
- The live service uses HTTPS and has tested timeout and request-size behavior.

### Phase 4 — Improve through careful feedback

**Outcome:** Future improvements respond to real user friction without expanding data collection unnecessarily.

**Work**

- Invite feedback about confusing results, missed sections, and the usefulness of recommendations.
- Review feedback in aggregate and turn recurring issues into test cases or documentation updates.
- Prioritize improvements by user impact, frequency, and confidence—not by feature count.
- Revisit whether any proposed capability changes the product's privacy, explainability, or decision-support boundaries.

**How we will know it helped**

- Repeated user-reported issues lead to reproducible test cases or clear product updates.
- Feedback processes continue to avoid collecting uploaded resume content by default.
- New work preserves the product's informational—not authoritative—role.

## 8. Prioritized work queue

| Priority | Work item | Why it matters | Completion signal |
|---|---|---|---|
| **P0 — Reliability** | Test varied resume layouts and improve section extraction | Weak extraction undermines every later score and suggestion | Sanitized fixtures and expected-output tests cover representative layouts |
| **P0 — Reliability** | Expand and test skill aliases and qualification parsing | Relevant terms can be overlooked or matched too loosely | Reviewed examples pass boundary-aware detection tests |
| **P1 — Analysis quality** | Improve experience-duration matching | Current date-range heuristics do not cover common requirement formats reliably | Tests cover plus-years, months, open ranges, and overlapping roles |
| **P1 — Validation** | Evaluate score components on a labeled, consented set | Weights should not be treated as meaningful without evidence | Evaluation findings and limitations are documented before score changes |
| **P1 — User experience** | Add frontend regression coverage | Input combinations and error rendering are important to a dependable workflow | Tests cover paste-only, combined inputs, errors, and rankings |
| **P2 — Deployment** | Set hosting limits, timeouts, HTTPS, and safe observability | Local memory handling alone does not define hosting behavior | Deployment checklist and configuration are verified for the target host |
| **P2 — Product feedback** | Gather privacy-conscious feedback on clarity and errors | Real friction should guide future improvements | Feedback process avoids resume retention and produces actionable themes |
| **P3 — Supply chain** | Decide whether to pin or self-host Bootstrap | External CDN use affects offline availability and deployment control | A documented decision matches the target deployment needs |

## 9. How we will measure progress

Success is not simply a higher match score or more features. Progress should be measured by the quality, clarity, and trustworthiness of the comparison.

### Reliability

- Supported file types, file-size limits, description lengths, and job-count limits behave consistently across the UI, API, and tests.
- Representative extraction and parsing cases have repeatable regression tests.
- Invalid and unreadable inputs produce explicit errors rather than incomplete success-shaped results.

### Usefulness

- Each analysis includes the five score dimensions, recognized matches and gaps, and ranked job recommendations.
- Suggestions help users identify a specific section or truthful next step to review.
- Users can understand that recognition can be incomplete and check the original source.

### Trust and privacy

- Product language consistently describes estimates, heuristics, and limitations.
- Uploaded content is not retained in application storage or exposed through raw-content logging.
- The product does not invent user qualifications or frame results as hiring outcomes.

### Maintainability

- Changes to parsing, scoring, ranking, or response structure have focused tests.
- User-facing documentation remains aligned with actual code behavior.
- The backend test suite passes and frontend JavaScript parses successfully.

## 10. Risks and safeguards

| Risk | Why it matters | Safeguard |
|---|---|---|
| **A match score appears more certain than it is** | Users may treat a heuristic as an objective verdict | Label estimates clearly, expose component explanations, and avoid hiring-outcome language |
| **A resume layout causes important evidence to be missed** | A low or incomplete result may mislead the user | Test varied layouts, show extracted information for review, and explain OCR/layout limits |
| **A skill is missed or matched incidentally** | Gaps and overlaps may be incomplete or noisy | Maintain reviewed aliases and boundary-aware tests; encourage verification against the posting |
| **Advice encourages unsupported resume claims** | Users may be led toward exaggeration | Use fill-in guidance grounded in real evidence; explicitly prohibit invented credentials and metrics |
| **Hosting behavior conflicts with privacy copy** | Infrastructure logs and request handling are outside the local parser | Review the chosen platform, configure privacy-safe observability, and align public copy with actual behavior |
| **External frontend assets are unavailable or change** | The page can lose styling or depend on a third-party delivery path | Decide whether to pin or self-host Bootstrap when deployment needs are known |

## 11. Release-readiness checklist

Before calling a release ready:

- [ ] Run `python -m pytest backend/tests -q`.
- [ ] Run `node --check frontend/app.js`.
- [ ] Run `git diff --check`.
- [ ] Verify supported file types, 5 MB upload limits, description character limits, and the 10-job maximum.
- [ ] Verify paste-only analysis and combined pasted/uploaded job descriptions.
- [ ] Verify readable validation errors, loading behavior, and ranked results in a browser.
- [ ] Confirm scores, limitations, privacy copy, and actual logging/storage behavior agree.
- [ ] Review detected resume details and suggestions for truthful, evidence-conscious wording.
- [ ] Confirm deployment uses HTTPS and has appropriate request-size and timeout controls.

## 12. Closing direction

The product should help people make a better-informed next move—not reduce their experience to a number. The strongest path forward is to make document understanding more dependable, make every estimate easier to inspect, and preserve privacy and honesty as the product grows.

**Build confidence first. Add breadth only when it makes the comparison clearer, safer, and more genuinely useful.**
