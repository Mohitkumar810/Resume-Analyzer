from io import BytesIO

from docx import Document
from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def make_docx(content: str) -> bytes:
    document = Document()
    document.add_paragraph(content)
    output = BytesIO()
    document.save(output)
    return output.getvalue()


def test_health_endpoint() -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyze_accepts_docx_and_returns_result_shape() -> None:
    resume = make_docx(
        "Software engineer with Python, FastAPI, SQL, Docker, and communication skills. "
        "Built reliable APIs and improved service performance for business teams."
    )
    response = client.post(
        "/api/analyze",
        files={"resume": ("resume.docx", resume, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
        data={
            "job_description": (
                "Seeking a Python engineer with FastAPI, SQL, Docker, and communication skills "
                "to build reliable APIs for business teams."
            )
        },
    )

    assert response.status_code == 200
    result = response.json()
    assert set(result) == {
        "job_title",
        "match_score",
        "score_breakdown",
        "matched_skills",
        "missing_skills",
        "preferred_skills",
        "matched_preferred_skills",
        "missing_preferred_skills",
        "required_skills",
        "resume_skills",
        "job_keywords",
        "skill_categories",
        "experience_requirements",
        "required_qualifications",
        "preferred_qualifications",
        "learning_roadmap",
        "suggestions",
        "resume_profile",
        "job_analyses",
        "recommendations",
    }
    assert result["matched_skills"] == ["Python", "FastAPI", "SQL", "Docker", "Communication"]
    assert result["resume_profile"]["technical_skills"]


def test_analyze_ranks_multiple_job_descriptions() -> None:
    resume = make_docx(
        "Jordan Lee\n"
        "SKILLS\nPython, SQL, FastAPI, Docker\n"
        "EDUCATION\nB.S. Computer Science\n"
        "EXPERIENCE\nBuilt Python APIs and improved performance by 30%."
    )
    response = client.post(
        "/api/analyze",
        files={"resume": ("resume.docx", resume, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
        data={
            "job_descriptions": [
                "Software Engineer\nRequired: Python, SQL, FastAPI, and Docker skills to build APIs.",
                "Marketing Manager\nRequired: Tableau, Power BI, and Excel skills to plan campaigns.",
            ]
        },
    )

    assert response.status_code == 200, response.text
    result = response.json()
    assert len(result["job_analyses"]) == 2
    assert result["recommendations"][0]["match_score"] >= result["recommendations"][1]["match_score"]
    assert result["job_title"] == result["recommendations"][0]["job_title"]


def test_analyze_accepts_uploaded_text_job_description() -> None:
    resume = make_docx("Python developer with SQL experience building software APIs for internal teams.")
    description = b"Backend Engineer\nSeeking a Python developer with SQL skills to build reliable software APIs."
    response = client.post(
        "/api/analyze",
        files=[
            ("resume", ("resume.docx", resume, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")),
            ("job_files", ("backend-role.txt", description, "text/plain")),
        ],
    )

    assert response.status_code == 200, response.text
    assert response.json()["job_analyses"][0]["job_title"] == "Backend Engineer"


def test_analyze_rejects_unsupported_file_type() -> None:
    response = client.post(
        "/api/analyze",
        files={"resume": ("resume.txt", b"plain text resume content", "text/plain")},
        data={"job_description": "This is a long enough job description for validation."},
    )

    assert response.status_code == 415
    assert response.json()["detail"] == "Upload a PDF or DOCX resume."


def test_analyze_rejects_short_job_description() -> None:
    response = client.post(
        "/api/analyze",
        files={"resume": ("resume.docx", make_docx("Python developer with enough content " * 4), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
        data={"job_description": "Too short"},
    )

    assert response.status_code == 422
    assert "at least 30 characters" in response.json()["detail"]
