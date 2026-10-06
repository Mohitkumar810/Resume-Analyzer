from backend.app.analyzer import analyze_match, analyze_resume, extract_skills


def test_extract_skills_uses_aliases_and_word_boundaries() -> None:
    skills = extract_skills("Built APIs with Python, FastAPI, and PostgreSQL. I enjoy pythonic code.")

    assert skills == ["Python", "FastAPI", "PostgreSQL"]


def test_analyze_match_returns_transparent_breakdown_and_gaps() -> None:
    result = analyze_match(
        "Python developer with FastAPI and SQL experience building REST APIs.",
        "We need a Python engineer with FastAPI, SQL, Docker, and communication skills.",
    )

    assert result["match_score"] in range(0, 101)
    assert result["matched_skills"] == ["Python", "FastAPI", "SQL"]
    assert result["missing_skills"] == ["Docker", "Communication"]
    assert result["score_breakdown"]["skill_coverage"] == 60
    assert result["job_keywords"]
    assert result["suggestions"]


def test_analyze_match_without_detected_skills_uses_text_similarity_only() -> None:
    result = analyze_match(
        "Experienced team contributor who builds useful products.",
        "A thoughtful applicant will build useful products for a growing organization.",
    )

    assert result["score_breakdown"]["skill_coverage"] is None
    assert "text similarity only" in result["score_breakdown"]["scoring_note"]


def test_analyze_match_separates_preferred_skills_and_builds_roadmap() -> None:
    resume = (
        "Python developer with SQL experience.\n"
        "EDUCATION\nB.S. in Computer Science from State University.\n"
        "EXPERIENCE\nBuilt a Python data service and improved response time by 20%."
    )
    description = (
        "Software Engineer\n"
        "Required qualifications:\nMust have 3 years of professional experience with Python, SQL, and Docker.\n"
        "Preferred qualifications:\nNice to have AWS and React experience."
    )

    result = analyze_match(resume, description)

    assert result["required_skills"] == ["Python", "SQL", "Docker"]
    assert result["preferred_skills"] == ["React", "AWS"]
    assert result["missing_skills"] == ["Docker"]
    assert result["learning_roadmap"][0]["skill"] == "Docker"
    assert result["experience_requirements"] == ["3 years of professional experience"]
    assert result["required_qualifications"] == [
        "Must have 3 years of professional experience with Python, SQL, and Docker."
    ]
    assert result["preferred_qualifications"] == ["Nice to have AWS and React experience."]
    assert set(result["score_breakdown"]) >= {
        "skills", "education", "experience", "projects", "keywords"
    }


def test_analyze_resume_extracts_sections_and_flags_missing_sections() -> None:
    profile = analyze_resume(
        "Jordan Lee\njordan@example.com\n"
        "SKILLS\nPython, SQL, Communication\n"
        "EDUCATION\nB.S. Computer Science, State University, 2022\n"
        "EXPERIENCE\nBuilt an API with Python and reduced processing time by 30%."
    )

    assert profile["name"] == "Jordan Lee"
    assert profile["technical_skills"] == ["Python", "SQL"]
    assert profile["soft_skills"] == ["Communication"]
    assert profile["education"]
    assert {item["section"] for item in profile["missing_weak_sections"]} >= {
        "projects", "certifications"
    }
