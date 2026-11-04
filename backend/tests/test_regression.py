import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.regression.regression_engine import RegressionEngine
from app.regression.regression_report import RegressionReport


client = TestClient(app)


def test_normalization():
    engine = RegressionEngine()

    assert engine.normalize("  HELLO   WORLD ") == "hello world"


def test_matching_answer_passes():
    engine = RegressionEngine()

    result = engine.evaluate_case({
        "test_id": "T001",
        "question": "What is Python?",
        "expected_answer": "Python is a language.",
        "actual_answer": "  Python is a language. "
    })

    assert result["passed"] is True
    assert result["status"] == "PASS"


def test_different_answer_fails():
    engine = RegressionEngine()

    result = engine.evaluate_case({
        "test_id": "T002",
        "question": "What is Python?",
        "expected_answer": "Python is a language.",
        "actual_answer": "Python is a database."
    })

    assert result["passed"] is False
    assert result["status"] == "FAIL"


def test_regression_detection():
    engine = RegressionEngine()

    previous = {
        "results": [
            {"test_id": "T001", "passed": True},
            {"test_id": "T002", "passed": True}
        ]
    }

    current = {
        "results": [
            {"test_id": "T001", "passed": False},
            {"test_id": "T002", "passed": True}
        ]
    }

    regressions = engine.detect_regressions(previous, current)

    assert regressions == ["T001"]


def test_existing_failure_is_not_new_regression():
    engine = RegressionEngine()

    previous = {
        "results": [
            {"test_id": "T001", "passed": False}
        ]
    }

    current = {
        "results": [
            {"test_id": "T001", "passed": False}
        ]
    }

    assert engine.detect_regressions(previous, current) == []


def test_unknown_suite_returns_404():
    response = client.post(
        "/api/v1/regression/run",
        json={"suite_name": "does_not_exist"}
    )

    assert response.status_code == 404


def test_suites_endpoint():
    response = client.get("/api/v1/regression/suites")

    assert response.status_code == 200

    names = [item["suite_name"] for item in response.json()["suites"]]

    assert "basic_qa" in names
    assert "negative_qa" in names


def test_report_history_and_regression(tmp_path):
    service = RegressionReport(report_dir=tmp_path)

    first = service.run("basic_qa")
    second = service.run("basic_qa")

    assert first["total_tests"] == 3
    assert first["passed"] == 3
    assert first["status"] == "PASS"

    assert second["total_tests"] == 3
    assert second["regression_count"] == 0

    history_file = tmp_path / "basic_qa_history.json"

    assert history_file.exists()


def test_report_rejects_unknown_suite(tmp_path):
    service = RegressionReport(report_dir=tmp_path)

    with pytest.raises(ValueError):
        service.run("unknown_suite")