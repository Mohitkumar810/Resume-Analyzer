const form = document.querySelector("#analysis-form");
const fileInput = document.querySelector("#resume");
const descriptionInput = document.querySelector("#job-description");
const characterCount = document.querySelector("#character-count");
const feedback = document.querySelector("#feedback");
const results = document.querySelector("#results");
const submitButton = document.querySelector("#submit-button");
const buttonLabel = submitButton.querySelector(".button-label");
const spinner = submitButton.querySelector(".spinner-border");

descriptionInput.addEventListener("input", () => {
  characterCount.textContent = `${descriptionInput.value.length.toLocaleString()} / 20,000`;
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  feedback.classList.add("d-none");
  results.classList.add("d-none");
  results.replaceChildren();
  setLoading(true);

  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      body: new FormData(form),
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "The analysis could not be completed.");
    }
    renderResults(payload);
  } catch (error) {
    showFeedback(error instanceof Error ? error.message : "The analysis could not be completed.", "danger");
  } finally {
    setLoading(false);
  }
});

function setLoading(isLoading) {
  submitButton.disabled = isLoading;
  buttonLabel.textContent = isLoading ? "Analyzing..." : "Analyze my match";
  spinner.classList.toggle("d-none", !isLoading);
}

function showFeedback(message, type) {
  feedback.className = `alert alert-${type} mt-4`;
  feedback.textContent = message;
}

function renderResults(data) {
  const card = document.createElement("div");
  card.className = "card result-card border-0 shadow-sm";
  const body = document.createElement("div");
  body.className = "card-body p-4 p-md-5";

  const scoreHeader = document.createElement("div");
  scoreHeader.className = "text-center pb-4";
  scoreHeader.append(
    makeText("p", "eyebrow mb-2", "YOUR MATCH OVERVIEW"),
    makeText("div", "score-number", `${data.match_score}%`),
    makeText("p", "text-secondary mt-2 mb-0", "Resume and job description similarity"),
  );
  body.append(scoreHeader);

  const breakdown = document.createElement("div");
  breakdown.className = "result-section py-4";
  breakdown.append(makeText("h3", "h6 fw-bold mb-3", "How the score is calculated"));
  breakdown.append(makeProgress("Text similarity", data.score_breakdown.text_similarity));
  if (data.score_breakdown.skill_coverage !== null) {
    breakdown.append(makeProgress("Detected skill coverage", data.score_breakdown.skill_coverage));
  }
  breakdown.append(makeText("p", "small text-secondary mb-0 mt-3", data.score_breakdown.scoring_note));
  body.append(breakdown);

  const matched = document.createElement("div");
  matched.className = "result-section py-4";
  matched.append(makeText("h3", "h6 fw-bold mb-2", `Matched skills (${data.matched_skills.length})`));
  appendChips(matched, data.matched_skills, "No matching dictionary skills were detected.");
  body.append(matched);

  const missing = document.createElement("div");
  missing.className = "result-section py-4";
  missing.append(makeText("h3", "h6 fw-bold mb-2", `Skills to consider (${data.missing_skills.length})`));
  appendChips(missing, data.missing_skills, "No missing dictionary skills were detected.");
  body.append(missing);

  const keywords = document.createElement("div");
  keywords.className = "result-section py-4";
  keywords.append(makeText("h3", "h6 fw-bold mb-2", "Job description keywords"));
  appendChips(keywords, data.job_keywords, "No keywords could be extracted.");
  body.append(keywords);

  const suggestions = document.createElement("div");
  suggestions.className = "result-section pt-4";
  suggestions.append(makeText("h3", "h6 fw-bold mb-2", "Ways to strengthen your application"));
  const list = document.createElement("ul");
  list.className = "mb-0 ps-3";
  for (const suggestion of data.suggestions) {
    list.append(makeText("li", "mb-2", suggestion));
  }
  suggestions.append(list);
  body.append(suggestions);

  card.append(body);
  results.append(card);
  results.classList.remove("d-none");
  results.scrollIntoView({ behavior: "smooth", block: "start" });
}

function makeProgress(label, value) {
  const wrapper = document.createElement("div");
  wrapper.className = "mb-3";
  const heading = document.createElement("div");
  heading.className = "d-flex justify-content-between small mb-1";
  heading.append(makeText("span", "fw-semibold", label), makeText("span", "", `${value}%`));
  const progress = document.createElement("div");
  progress.className = "progress";
  progress.setAttribute("role", "progressbar");
  progress.setAttribute("aria-label", label);
  progress.setAttribute("aria-valuenow", String(value));
  progress.setAttribute("aria-valuemin", "0");
  progress.setAttribute("aria-valuemax", "100");
  const bar = document.createElement("div");
  bar.className = "progress-bar";
  bar.style.width = `${value}%`;
  progress.append(bar);
  wrapper.append(heading, progress);
  return wrapper;
}

function appendChips(container, values, emptyMessage) {
  if (values.length === 0) {
    container.append(makeText("p", "small text-secondary mb-0", emptyMessage));
    return;
  }
  for (const value of values) {
    const chip = makeText("span", "skill-chip", value);
    if (container.querySelector("h3")?.textContent.startsWith("Skills to consider")) {
      chip.classList.add("missing");
    }
    container.append(chip);
  }
}

function makeText(tag, className, text) {
  const element = document.createElement(tag);
  element.className = className;
  element.textContent = text;
  return element;
}
