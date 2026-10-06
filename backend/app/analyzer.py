from __future__ import annotations

import re
from datetime import date

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SKILL_ALIASES: dict[str, tuple[str, ...]] = {
    "Python": ("python",),
    "JavaScript": ("javascript", "js"),
    "TypeScript": ("typescript",),
    "Java": ("java",),
    "C++": ("c++",),
    "C#": ("c#", "c sharp"),
    "Go": ("golang",),
    "HTML": ("html",),
    "CSS": ("css",),
    "Bootstrap": ("bootstrap",),
    "React": ("react", "react.js", "reactjs"),
    "Angular": ("angular",),
    "Vue.js": ("vue.js", "vuejs"),
    "Node.js": ("node.js", "nodejs"),
    "FastAPI": ("fastapi",),
    "Flask": ("flask",),
    "Django": ("django",),
    "Spring": ("spring framework", "spring boot"),
    "SQL": ("sql",),
    "PostgreSQL": ("postgresql", "postgres"),
    "MySQL": ("mysql",),
    "SQLite": ("sqlite",),
    "MongoDB": ("mongodb", "mongo"),
    "Redis": ("redis",),
    "AWS": ("aws", "amazon web services"),
    "Azure": ("microsoft azure", "azure"),
    "Google Cloud": ("google cloud", "gcp"),
    "Docker": ("docker",),
    "Kubernetes": ("kubernetes", "k8s"),
    "Git": ("git", "github", "gitlab"),
    "Linux": ("linux",),
    "CI/CD": ("ci/cd", "continuous integration", "continuous deployment"),
    "REST APIs": ("rest api", "rest apis", "restful api", "restful apis"),
    "GraphQL": ("graphql",),
    "Data analysis": ("data analysis", "data analytics"),
    "Machine learning": ("machine learning", "ml"),
    "NLP": ("natural language processing", "nlp"),
    "Pandas": ("pandas",),
    "scikit-learn": ("scikit-learn", "sklearn"),
    "TensorFlow": ("tensorflow",),
    "PyTorch": ("pytorch",),
    "Excel": ("microsoft excel", "excel"),
    "Tableau": ("tableau",),
    "Power BI": ("power bi",),
    "Jira": ("jira",),
    "Figma": ("figma",),
    "Project management": ("project management",),
    "Agile": ("agile", "scrum"),
    "Communication": ("communication", "interpersonal skills", "verbal communication"),
    "Leadership": ("leadership", "team leadership"),
    "Teamwork": ("teamwork", "collaboration", "collaborative"),
    "Problem solving": ("problem solving", "problem-solving", "analytical thinking"),
    "Adaptability": ("adaptability", "flexibility"),
    "Time management": ("time management", "prioritization"),
    "Creativity": ("creativity", "creative thinking"),
}

SKILL_CATEGORIES: dict[str, str] = {
    "Python": "Programming", "JavaScript": "Programming", "TypeScript": "Programming",
    "Java": "Programming", "C++": "Programming", "C#": "Programming", "Go": "Programming",
    "HTML": "Programming", "CSS": "Programming", "SQL": "Databases",
    "PostgreSQL": "Databases", "MySQL": "Databases", "SQLite": "Databases",
    "MongoDB": "Databases", "Redis": "Databases", "AWS": "Cloud", "Azure": "Cloud",
    "Google Cloud": "Cloud", "React": "Frameworks", "Angular": "Frameworks",
    "Vue.js": "Frameworks", "Node.js": "Frameworks", "FastAPI": "Frameworks",
    "Flask": "Frameworks", "Django": "Frameworks", "Spring": "Frameworks",
    "Bootstrap": "Frameworks", "Docker": "DevOps & Tools", "Kubernetes": "DevOps & Tools",
    "Git": "DevOps & Tools", "Linux": "DevOps & Tools", "CI/CD": "DevOps & Tools",
    "Jira": "DevOps & Tools", "Figma": "DevOps & Tools", "REST APIs": "Frameworks",
    "GraphQL": "Frameworks", "Data analysis": "Data & Analytics",
    "Machine learning": "Data & Analytics", "NLP": "Data & Analytics", "Pandas": "Data & Analytics",
    "scikit-learn": "Data & Analytics", "TensorFlow": "Data & Analytics",
    "PyTorch": "Data & Analytics", "Excel": "Data & Analytics", "Tableau": "Data & Analytics",
    "Power BI": "Data & Analytics", "Project management": "Ways of Working",
    "Agile": "Ways of Working", "Communication": "Soft Skills", "Leadership": "Soft Skills",
    "Teamwork": "Soft Skills", "Problem solving": "Soft Skills", "Adaptability": "Soft Skills",
    "Time management": "Soft Skills", "Creativity": "Soft Skills",
}

SECTION_ALIASES: dict[str, tuple[str, ...]] = {
    "education": ("education", "academic background", "academic qualifications"),
    "experience": ("experience", "work experience", "employment history", "professional experience"),
    "projects": ("projects", "personal projects", "academic projects", "project experience"),
    "certifications": ("certifications", "certificates", "licenses", "licenses & certifications"),
    "skills": ("skills", "technical skills", "core competencies", "technologies"),
}

NON_ANALYZED_HEADINGS = {
    "contact", "summary", "professional summary", "profile", "objective",
    "interests", "languages", "awards", "publications", "references",
}
PREFERRED_MARKERS = ("preferred", "nice to have", "nice-to-have", "bonus", "desired", "ideally")


def extract_skills(text: str) -> list[str]:
    return [
        skill
        for skill, aliases in SKILL_ALIASES.items()
        if any(_contains_phrase(text, alias) for alias in aliases)
    ]


def analyze_resume(resume_text: str) -> dict[str, object]:
    sections = _extract_sections(resume_text)
    resume_skills = extract_skills(resume_text)
    missing_weak_sections: list[dict[str, str]] = []
    for section in ("education", "experience", "projects", "skills"):
        content = sections[section]
        if not content:
            missing_weak_sections.append({"section": section, "status": "missing"})
        elif len(content) < 60 or (
            section in {"experience", "projects"} and not _has_impact_evidence(content)
        ):
            missing_weak_sections.append({"section": section, "status": "weak"})
    if not sections["certifications"]:
        missing_weak_sections.append({"section": "certifications", "status": "missing"})

    return {
        "name": _extract_name(resume_text),
        "education": sections["education"],
        "experience": sections["experience"],
        "projects": sections["projects"],
        "certifications": sections["certifications"],
        "skills": resume_skills,
        "technical_skills": [
            skill for skill in resume_skills if SKILL_CATEGORIES.get(skill) != "Soft Skills"
        ],
        "soft_skills": [
            skill for skill in resume_skills if SKILL_CATEGORIES.get(skill) == "Soft Skills"
        ],
        "skills_by_category": _group_skills(resume_skills),
        "missing_weak_sections": missing_weak_sections,
    }


def analyze_match(
    resume_text: str,
    job_description: str,
    resume_profile: dict[str, object] | None = None,
) -> dict[str, object]:
    resume_profile = resume_profile or analyze_resume(resume_text)
    resume_skills = extract_skills(resume_text)
    all_job_skills = extract_skills(job_description)
    preferred_text = _preferred_text(job_description)
    preferred_skills = [skill for skill in all_job_skills if _contains_phrase(preferred_text, skill)]
    required_skills = [skill for skill in all_job_skills if skill not in preferred_skills]
    matched_skills = [skill for skill in required_skills if skill in resume_skills]
    missing_skills = [skill for skill in required_skills if skill not in resume_skills]
    matched_preferred = [skill for skill in preferred_skills if skill in resume_skills]
    missing_preferred = [skill for skill in preferred_skills if skill not in resume_skills]

    text_similarity = _text_similarity(resume_text, job_description)
    skill_coverage = len(matched_skills) / len(required_skills) if required_skills else None
    skills_score = round((skill_coverage if skill_coverage is not None else text_similarity) * 100)
    sections = _extract_sections(resume_text)
    education_score = _relevance_score(sections["education"], job_description)
    experience_score = _experience_score(sections["experience"], job_description)
    projects_score = _relevance_score(sections["projects"], job_description)
    keyword_score = _keyword_score(resume_text, job_description)
    score_breakdown = {
        "skills": skills_score,
        "education": education_score,
        "experience": experience_score,
        "projects": projects_score,
        "keywords": keyword_score,
        "text_similarity": round(text_similarity * 100),
        "skill_coverage": round(skill_coverage * 100) if skill_coverage is not None else None,
        "scoring_note": (
            "No dictionary skills were detected in the job description; the skills score uses text similarity only. "
            "This heuristic is not a hiring decision."
            if skill_coverage is None
            else "Heuristic estimate based on detected skills, section evidence, job keywords, and text similarity; "
            "it is not a hiring decision."
        ),
    }
    overall_score = round(
        score_breakdown["skills"] * 0.30
        + education_score * 0.15
        + experience_score * 0.20
        + projects_score * 0.15
        + keyword_score * 0.20
    )
    job_title = _extract_job_title(job_description)
    return {
        "job_title": job_title,
        "match_score": overall_score,
        "score_breakdown": score_breakdown,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "preferred_skills": preferred_skills,
        "matched_preferred_skills": matched_preferred,
        "missing_preferred_skills": missing_preferred,
        "required_skills": required_skills,
        "resume_skills": resume_skills,
        "job_keywords": _extract_keywords(job_description),
        "skill_categories": _group_skills(all_job_skills),
        "experience_requirements": _extract_experience_requirements(job_description),
        "required_qualifications": _extract_required_qualifications(job_description),
        "preferred_qualifications": _extract_preferred_qualifications(job_description),
        "learning_roadmap": _build_roadmap(missing_skills),
        "suggestions": _build_suggestions(missing_skills, resume_profile),
    }


def _extract_sections(text: str) -> dict[str, str]:
    lines = text.splitlines()
    sections = {name: "" for name in SECTION_ALIASES}
    active_section: str | None = None
    collected: dict[str, list[str]] = {name: [] for name in SECTION_ALIASES}
    for line in lines:
        stripped = line.strip()
        normalized = re.sub(r"[^a-z& ]", "", stripped.casefold()).strip()
        heading = next(
            (
                section
                for section, aliases in SECTION_ALIASES.items()
                if normalized in aliases
            ),
            None,
        )
        if heading:
            active_section = heading
        elif normalized in NON_ANALYZED_HEADINGS:
            active_section = None
        elif active_section and stripped:
            collected[active_section].append(stripped)
    for section, content in collected.items():
        sections[section] = "\n".join(content)
    return sections


def _extract_name(text: str) -> str | None:
    for line in text.splitlines():
        candidate = line.strip()
        if not candidate or len(candidate) > 70 or "@" in candidate or "://" in candidate:
            continue
        if re.search(r"\d", candidate) or "|" in candidate or _is_section_heading(candidate):
            continue
        words = candidate.split()
        if (
            2 <= len(words) <= 4
            and not re.search(
                r"\b(engineer|developer|designer|analyst|manager|scientist|specialist|consultant|intern|resume)\b",
                candidate,
                re.I,
            )
            and all(re.fullmatch(r"[A-Za-z][A-Za-z.'-]*", word) for word in words)
        ):
            return candidate
    return None


def _is_section_heading(text: str) -> bool:
    normalized = re.sub(r"[^a-z& ]", "", text.casefold()).strip()
    return any(normalized in aliases for aliases in SECTION_ALIASES.values())


def _has_impact_evidence(text: str) -> bool:
    return bool(re.search(r"\b(increased|reduced|improved|built|developed|led|created|delivered|achieved|launched|automated|saved|result(?:ed)?|%|\d+)\b", text, re.I))


def _group_skills(skills: list[str]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {}
    for skill in skills:
        grouped.setdefault(SKILL_CATEGORIES.get(skill, "Other"), []).append(skill)
    return grouped


def _preferred_text(text: str) -> str:
    preferred_lines: list[str] = []
    in_preferred_section = False
    for line in text.splitlines():
        normalized = line.strip().casefold()
        if any(marker in normalized for marker in PREFERRED_MARKERS):
            in_preferred_section = True
            preferred_lines.append(line)
        elif normalized.rstrip(":") in {
            "requirements", "required qualifications", "minimum qualifications",
            "responsibilities", "what you will do",
        }:
            in_preferred_section = False
        elif in_preferred_section:
            preferred_lines.append(line)
    return "\n".join(preferred_lines)


def _extract_preferred_qualifications(text: str) -> list[str]:
    qualifications: list[str] = []
    for line in _preferred_text(text).splitlines():
        qualification = line.strip(" \t-*•")
        if not qualification:
            continue
        if re.fullmatch(r"(?:preferred|nice to have|desired|bonus)(?: qualifications?)?:?", qualification, re.I):
            continue
        qualifications.append(qualification)
    return qualifications[:8]


def _extract_required_qualifications(text: str) -> list[str]:
    qualifications: list[str] = []
    in_required_section = False
    for line in text.splitlines():
        qualification = line.strip(" \t-*•")
        normalized = qualification.casefold().rstrip(":")
        if not qualification:
            continue
        if any(marker in normalized for marker in PREFERRED_MARKERS):
            in_required_section = False
        elif normalized in {
            "requirements", "required qualifications", "minimum qualifications",
            "qualifications", "what we need",
        }:
            in_required_section = True
        elif normalized in {"responsibilities", "what you will do", "what you'll do"}:
            in_required_section = False
        elif in_required_section or re.search(
            r"\b(required|must have|minimum qualification|requirement)\b", qualification, re.I
        ):
            qualifications.append(qualification)
    return qualifications[:8]


def _extract_experience_requirements(text: str) -> list[str]:
    pattern = re.compile(
        r"\b(?:at least\s+)?\d+(?:\s*[-–]\s*\d+)?\+?\s+years?\s+"
        r"(?:of\s+)?(?:relevant\s+|professional\s+)?(?:experience|work experience)\b",
        re.I,
    )
    return list(dict.fromkeys(match.group(0) for match in pattern.finditer(text)))


def _extract_job_title(text: str) -> str:
    for line in text.splitlines():
        candidate = line.strip(" \t-*•:#")
        if candidate and len(candidate) <= 90 and re.search(
            r"\b(engineer|developer|designer|analyst|manager|scientist|administrator|specialist|intern)\b",
            candidate,
            re.I,
        ):
            return candidate
    return "Job opportunity"


def _relevance_score(section_text: str, job_description: str) -> int:
    if not section_text:
        return 0
    return round(_text_similarity(section_text, job_description) * 100)


def _experience_score(experience_text: str, job_description: str) -> int:
    if not experience_text:
        return 0
    requested = _extract_experience_requirements(job_description)
    years_match = re.search(r"\b(\d{4})\s*[-–]\s*(?:\d{4}|present|current)\b", experience_text, re.I)
    if requested and years_match:
        years_value = re.search(r"\d+", requested[0])
        required_years = int(years_value.group()) if years_value else 1
        start_year = int(years_match.group(1))
        end_match = re.search(r"[-–]\s*(\d{4})", years_match.group())
        estimated_years = (int(end_match.group(1)) if end_match else date.today().year) - start_year
        return min(100, round(estimated_years / max(required_years, 1) * 100))
    return _relevance_score(experience_text, job_description)


def _keyword_score(resume_text: str, job_description: str) -> int:
    keywords = _extract_keywords(job_description)
    if not keywords:
        return 0
    found = sum(1 for keyword in keywords if _contains_phrase(resume_text, keyword))
    return round(found / len(keywords) * 100)


def _build_roadmap(missing_skills: list[str]) -> list[dict[str, str]]:
    return [
        {
            "skill": skill,
            "category": SKILL_CATEGORIES.get(skill, "Other"),
            "action": f"Learn the fundamentals of {skill}, then build a small project that demonstrates it.",
            "timeframe": "1–2 weeks",
        }
        for skill in missing_skills
    ]


def _build_suggestions(
    missing_skills: list[str], resume_profile: dict[str, object]
) -> list[str]:
    suggestions: list[str] = []
    for item in resume_profile["missing_weak_sections"]:
        section = item["section"]
        status = item["status"]
        suggestions.append(
            f"{section.title()} section is {status}: "
            + (
                "add a concise section with relevant, accurate details."
                if status == "missing"
                else "add specific responsibilities, tools, and outcomes to strengthen it."
            )
        )
    if missing_skills:
        suggestions.append(
            f"If accurate, add evidence for {', '.join(missing_skills[:6])} in the project or experience "
            "where you used each skill; do not list skills you have not used."
        )
    suggestions.append(
        "Replace vague bullets such as “Worked on a college project” with "
        "“Developed [what] using [tools] to [solve which problem], resulting in [measurable outcome].” "
        "Fill in the brackets with truthful, specific details."
    )
    return suggestions


def _contains_phrase(text: str, phrase: str) -> bool:
    pattern = re.escape(phrase).replace(r"\ ", r"\s+")
    return re.search(rf"(?<![A-Za-z0-9]){pattern}(?![A-Za-z0-9])", text, re.IGNORECASE) is not None


def _text_similarity(resume_text: str, job_description: str) -> float:
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    try:
        vectors = vectorizer.fit_transform([resume_text, job_description])
    except ValueError:
        return 0.0
    return float(cosine_similarity(vectors[0:1], vectors[1:2])[0, 0])


def _extract_keywords(text: str) -> list[str]:
    vectorizer = TfidfVectorizer(stop_words="english", max_features=8)
    try:
        vectorizer.fit([text])
    except ValueError:
        return []
    return sorted(vectorizer.get_feature_names_out().tolist(), key=str.casefold)
