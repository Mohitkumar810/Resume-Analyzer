from __future__ import annotations

import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SKILL_ALIASES: dict[str, tuple[str, ...]] = {
    "Python": ("python",),
    "JavaScript": ("javascript", "js"),
    "TypeScript": ("typescript",),
    "HTML": ("html",),
    "CSS": ("css",),
    "Bootstrap": ("bootstrap",),
    "React": ("react",),
    "Node.js": ("node.js", "nodejs"),
    "FastAPI": ("fastapi",),
    "Flask": ("flask",),
    "SQL": ("sql",),
    "PostgreSQL": ("postgresql", "postgres"),
    "MySQL": ("mysql",),
    "SQLite": ("sqlite",),
    "MongoDB": ("mongodb", "mongo"),
    "AWS": ("aws", "amazon web services"),
    "Docker": ("docker",),
    "Kubernetes": ("kubernetes", "k8s"),
    "Git": ("git",),
    "Linux": ("linux",),
    "CI/CD": ("ci/cd", "continuous integration", "continuous deployment"),
    "REST APIs": ("rest api", "rest apis", "restful api", "restful apis"),
    "Data analysis": ("data analysis", "data analytics"),
    "Machine learning": ("machine learning", "ml"),
    "NLP": ("natural language processing", "nlp"),
    "Pandas": ("pandas",),
    "scikit-learn": ("scikit-learn", "sklearn"),
    "TensorFlow": ("tensorflow",),
    "PyTorch": ("pytorch",),
    "Excel": ("microsoft excel", "excel"),
    "Project management": ("project management",),
    "Agile": ("agile", "scrum"),
    "Communication": ("communication", "interpersonal skills"),
    "Leadership": ("leadership",),
}


def extract_skills(text: str) -> list[str]:
    found: list[str] = []
    for skill, aliases in SKILL_ALIASES.items():
        if any(_contains_phrase(text, alias) for alias in aliases):
            found.append(skill)
    return found


def analyze_match(resume_text: str, job_description: str) -> dict[str, object]:
    resume_skills = extract_skills(resume_text)
    required_skills = extract_skills(job_description)
    matched_skills = [skill for skill in required_skills if skill in resume_skills]
    missing_skills = [skill for skill in required_skills if skill not in resume_skills]

    text_similarity = _text_similarity(resume_text, job_description)
    skill_coverage = (
        len(matched_skills) / len(required_skills) if required_skills else None
    )
    if skill_coverage is None:
        overall_score = text_similarity
        scoring_note = "No dictionary skills were detected in the job description; score uses text similarity only."
    else:
        overall_score = (0.6 * text_similarity) + (0.4 * skill_coverage)
        scoring_note = "Score combines 60% text similarity and 40% coverage of detected job skills."

    return {
        "match_score": round(overall_score * 100),
        "score_breakdown": {
            "text_similarity": round(text_similarity * 100),
            "skill_coverage": round(skill_coverage * 100) if skill_coverage is not None else None,
            "scoring_note": scoring_note,
        },
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "resume_skills": resume_skills,
        "job_keywords": _extract_keywords(job_description),
        "suggestions": _build_suggestions(missing_skills),
    }


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


def _build_suggestions(missing_skills: list[str]) -> list[str]:
    if missing_skills:
        return [
            "If you have relevant experience with any missing skills, make that evidence easy to find in your resume. Do not add skills you do not have.",
            f"Consider addressing these job skills where truthful: {', '.join(missing_skills[:6])}.",
            "Use specific outcomes or metrics to show the impact of your work.",
        ]
    return [
        "Your resume includes the skills recognized in this job description; make sure each is supported by concrete experience.",
        "Add measurable outcomes to your strongest experience bullets.",
        "Tailor your summary to emphasize the responsibilities and keywords in this role.",
    ]
