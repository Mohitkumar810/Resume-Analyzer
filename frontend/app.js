const form = document.querySelector("#analysis-form");
const fileInput = document.querySelector("#resume");
const jobFilesInput = document.querySelector("#job-files");
const jobList = document.querySelector("#job-list");
const jobTemplate = document.querySelector("#job-template");
const addJobButton = document.querySelector("#add-job");
const feedback = document.querySelector("#feedback");
const results = document.querySelector("#results");
const submitButton = document.querySelector("#submit-button");
const buttonLabel = submitButton.querySelector(".button-label");
const spinner = submitButton.querySelector(".spinner-border");

addJobCard();

addJobButton.addEventListener("click", () => {
  if (jobList.querySelectorAll(".job-input").length >= 10) {
    showFeedback("Analyze up to 10 job descriptions at a time.", "warning");
    return;
  }
  addJobCard();
});

jobFilesInput.addEventListener("change", updateJobInputs);

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  feedback.classList.add("d-none");
  results.classList.add("d-none");
  results.replaceChildren();
  const textCount = [...jobList.querySelectorAll(".job-description")].filter(
    (input) => input.value.trim(),
  ).length;
  if (textCount + jobFilesInput.files.length > 10) {
    showFeedback("Analyze up to 10 job descriptions at a time.", "warning");
    return;
  }
  setLoading(true);

  try {
    const formData = new FormData(form);
    if (jobFilesInput.files.length === 0) {
      formData.delete("job_files");
    }
    const response = await fetch("/api/analyze", {
      method: "POST",
      body: formData,
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

function addJobCard() {
  const card = jobTemplate.content.firstElementChild.cloneNode(true);
  const textarea = card.querySelector(".job-description");
  textarea.addEventListener("input", () => {
    card.querySelector(".character-count").textContent =
      `${textarea.value.length.toLocaleString()} / 20,000`;
    updateJobInputs();
  });
  card.querySelector(".remove-job").addEventListener("click", () => {
    card.remove();
    updateJobInputs();
  });
  jobList.append(card);
  updateJobInputs();
}

function updateJobInputs() {
  const cards = [...jobList.querySelectorAll(".job-input")];
  const hasUploadedDescriptions = jobFilesInput.files.length > 0;
  cards.forEach((card, index) => {
    card.querySelector(".job-number").textContent = cards.length > 1 ? `${index + 1}` : "";
    card.querySelector(".remove-job").classList.toggle("d-none", cards.length === 1);
    card.querySelector(".job-description").required = index === 0 && !hasUploadedDescriptions;
  });
  addJobButton.disabled = cards.length >= 10;
}

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

  const ranking = document.createElement("section");
  ranking.className = "result-section pb-4";
  ranking.append(makeText("h2", "h5 fw-bold mb-3", "Job recommendations"));
  const rankedJobs = data.recommendations;
  rankedJobs.forEach((job, index) => {
    const recommendation = document.createElement("div");
    recommendation.className = "recommendation d-flex justify-content-between align-items-start gap-3";
    const details = document.createElement("div");
    details.append(
      makeText("div", "fw-semibold", `${index + 1}. ${job.job_title}`),
      makeText("div", "small text-secondary", `${job.matched_skills.length} required skills matched`),
    );
    recommendation.append(details, makeText("span", "recommendation-score", `${job.match_score}%`));
    ranking.append(recommendation);
  });
  body.append(ranking);

  const scoreHeader = document.createElement("div");
  scoreHeader.className = "text-center py-4";
  scoreHeader.append(
    makeText("p", "eyebrow mb-2", "TOP JOB MATCH"),
    makeText("div", "score-number", `${rankedJobs[0].match_score}%`),
    makeText("p", "text-secondary mt-2 mb-0", rankedJobs[0].job_title),
  );
  body.append(scoreHeader);

  const breakdown = document.createElement("section");
  breakdown.className = "result-section py-4";
  breakdown.append(makeText("h3", "h6 fw-bold mb-3", "Match score breakdown"));
  for (const key of ["skills", "education", "experience", "projects", "keywords"]) {
    breakdown.append(makeProgress(key[0].toUpperCase() + key.slice(1), data.score_breakdown[key]));
  }
  breakdown.append(makeText("p", "small text-secondary mb-0 mt-3", data.score_breakdown.scoring_note));
  body.append(breakdown);

  appendSkillSection(body, "Required skills matched", data.matched_skills, "No required skills matched.");
  appendSkillSection(body, "Missing required skills", data.missing_skills, "No required skill gaps detected.", true);
  appendSkillSection(body, "Preferred skills", data.preferred_skills, "No preferred skills detected.");

  const jobDetails = document.createElement("section");
  jobDetails.className = "result-section py-4";
  jobDetails.append(makeText("h3", "h6 fw-bold mb-3", "Job description analysis"));
  appendGroupedSkills(jobDetails, data.skill_categories);
  if (data.experience_requirements.length) {
    jobDetails.append(makeText("p", "small mb-2", `Experience requested: ${data.experience_requirements.join(", ")}`));
  } else {
    jobDetails.append(makeText("p", "small text-secondary mb-2", "No explicit years-of-experience requirement detected."));
  }
  appendList(jobDetails, "Required qualifications", data.required_qualifications);
  appendList(jobDetails, "Preferred qualifications", data.preferred_qualifications);
  body.append(jobDetails);

  const profile = document.createElement("section");
  profile.className = "result-section py-4";
  profile.append(makeText("h3", "h6 fw-bold mb-3", "Resume analysis"));
  const resumeProfile = data.resume_profile;
  if (resumeProfile.name) profile.append(makeText("p", "mb-2", `Name: ${resumeProfile.name}`));
  profile.append(
    makeText("p", "small mb-2", `Technical skills: ${resumeProfile.technical_skills.join(", ") || "None detected"}`),
    makeText("p", "small mb-2", `Soft skills: ${resumeProfile.soft_skills.join(", ") || "None detected"}`),
  );
  appendGroupedSkills(profile, resumeProfile.skills_by_category);
  appendList(profile, "Education", resumeProfile.education ? [resumeProfile.education] : []);
  appendList(profile, "Experience", resumeProfile.experience ? [resumeProfile.experience] : []);
  appendList(profile, "Projects", resumeProfile.projects ? [resumeProfile.projects] : []);
  appendList(profile, "Certifications", resumeProfile.certifications ? [resumeProfile.certifications] : []);
  if (resumeProfile.missing_weak_sections.length) {
    profile.append(makeText("h4", "small fw-bold mt-3", "Sections to strengthen"));
    const list = document.createElement("ul");
    list.className = "small mb-0 ps-3";
    resumeProfile.missing_weak_sections.forEach((section) => {
      list.append(makeText("li", "mb-1", `${section.section}: ${section.status}`));
    });
    profile.append(list);
  }
  body.append(profile);

  if (data.learning_roadmap.length) {
    const roadmap = document.createElement("section");
    roadmap.className = "result-section py-4";
    roadmap.append(makeText("h3", "h6 fw-bold mb-3", "Skill-gap learning roadmap"));
    const list = document.createElement("ul");
    list.className = "mb-0 ps-3";
    data.learning_roadmap.forEach((step) => {
      list.append(makeText("li", "mb-2", `${step.skill} (${step.category}, ${step.timeframe}): ${step.action}`));
    });
    roadmap.append(list);
    body.append(roadmap);
  }

  const suggestions = document.createElement("section");
  suggestions.className = "result-section pt-4";
  suggestions.append(makeText("h3", "h6 fw-bold mb-2", "Specific resume improvements"));
  const suggestionList = document.createElement("ul");
  suggestionList.className = "mb-0 ps-3";
  data.suggestions.forEach((suggestion) => {
    suggestionList.append(makeText("li", "mb-2", suggestion));
  });
  suggestions.append(suggestionList);
  body.append(suggestions);

  card.append(body);
  results.append(card);
  results.classList.remove("d-none");
  results.scrollIntoView({ behavior: "smooth", block: "start" });
}

function appendSkillSection(parent, title, skills, emptyMessage, missing = false) {
  const section = document.createElement("section");
  section.className = "result-section py-4";
  section.append(makeText("h3", "h6 fw-bold mb-2", `${title} (${skills.length})`));
  appendChips(section, skills, emptyMessage, missing);
  parent.append(section);
}

function appendGroupedSkills(parent, categories) {
  Object.entries(categories).forEach(([category, skills]) => {
    const row = document.createElement("div");
    row.className = "mb-2";
    row.append(makeText("span", "small fw-semibold me-2", `${category}:`));
    appendChips(row, skills, "");
    parent.append(row);
  });
}

function appendList(parent, title, items) {
  parent.append(makeText("h4", "small fw-bold mt-3", title));
  if (!items.length) {
    parent.append(makeText("p", "small text-secondary mb-0", "No section text detected."));
    return;
  }
  items.forEach((item) => parent.append(makeText("p", "small text-secondary mb-2 preserve-lines", item)));
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

function appendChips(container, values, emptyMessage, missing = false) {
  if (values.length === 0) {
    if (emptyMessage) container.append(makeText("p", "small text-secondary mb-0", emptyMessage));
    return;
  }
  values.forEach((value) => {
    const chip = makeText("span", "skill-chip", value);
    if (missing) chip.classList.add("missing");
    container.append(chip);
  });
}

function makeText(tag, className, text) {
  const element = document.createElement(tag);
  element.className = className;
  element.textContent = text;
  return element;
}
