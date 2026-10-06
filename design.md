# Product and UI Design

## Design intent

Make resume-to-job comparison feel private, calm, understandable, and actionable. The interface should help applicants inspect evidence and possible gaps, not imply automated hiring authority.

## Visual system

- **Brand:** ResumeMatch.
- **Palette:** light blue-gray page background (`#f5f7fc`), white cards, dark navy text (`#172b4d`), muted secondary text (`#66758c`), and indigo primary actions (`#4659d8`).
- **Typography:** system/Bootstrap sans-serif; bold, tightly tracked hero heading; small uppercase, letter-spaced indigo eyebrow labels.
- **Surfaces:** rounded white cards with subtle borders/shadows; soft indigo skill chips; warm pale-orange missing-skill chips.
- **Layout:** centered responsive content, constrained reading width, a concise hero, one primary form card, followed by results in clear sections.
- **Implementation:** Bootstrap 5.3.3 CDN plus project overrides in `frontend/styles.css`. No custom icon or component library.

## Page structure

1. **Header:** product wordmark and privacy/explainability descriptor.
2. **Hero:** clear promise that users can compare roles and learn what to strengthen.
3. **Input card:**
   - required PDF/DOCX resume upload with size and scanned-PDF guidance;
   - one or more removable, dynamically numbered pasted-description fields;
   - optional multi-file PDF/DOCX/TXT job-description upload;
   - primary analyze button, spinner, and per-field character counts;
   - limit of 10 total jobs.
4. **Feedback:** inline accessible error/status message.
5. **Results:**
   - ranked job recommendation list with scores;
   - top-job match score and five weighted component progress bars;
   - matched, missing required, and preferred skill chips;
   - job qualifications and categorized skills;
   - resume profile and weak/missing sections;
   - missing-skill learning roadmap;
   - specific resume improvement suggestions.
6. **Privacy disclaimer:** heuristic estimates, no hiring decision, truthful edits, and no retained resume or analysis.

## Interaction and responsive behavior

- Start with one required pasted-description field. The field becomes optional when there is another usable input, such as an uploaded job file.
- Add/remove description fields without leaving the page; disallow adding beyond 10 pasted fields and validate the combined pasted/uploaded count on submit.
- While a request is in flight, disable the submit button and show the analyzing state. Display API errors inline and restore the button after completion.
- On success, replace stale results, render the latest analysis, and scroll the results into view.
- Use a single-column form/results presentation on small screens. Keep recommendation scores visible without forcing horizontal scrolling.

## Accessibility and content

- Associate labels with file inputs and textareas, use real buttons for actions, and provide live regions for feedback/results.
- Represent component scores with named progress bars and explicit numeric values.
- Use text labels as well as color for matched versus missing skills.
- Never imply certainty. Use terms such as “estimated,” “detected,” and “heuristic”; encourage users to verify extracted details.
- Resume improvement advice must use a fill-in template and must not invent achievements, metrics, or credentials.

## Design constraints

- Keep content readable without a chart or color-only encoding.
- Keep externally loaded Bootstrap CDN availability in mind; consider pinning/self-hosting it if deployment requirements demand offline or supply-chain-controlled assets.
- Long extracted sections must wrap and remain readable. Do not insert extracted text as HTML.
