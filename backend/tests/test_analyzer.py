from backend.app.analyzer import analyze_match, extract_skills


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
        "A thoughtful contributor will build useful products with a collaborative team.",
    )

    assert result["score_breakdown"]["skill_coverage"] is None
    assert "text similarity only" in result["score_breakdown"]["scoring_note"]
