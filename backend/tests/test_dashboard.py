from fastapi.testclient import TestClient

from app.main import app
from app.dashboard.dashboard_service import find_metrics


client = TestClient(app)


def test_dashboard_endpoint():
    response = client.get("/api/v1/dashboard/summary")

    assert response.status_code == 200

    data = response.json()

    assert "total_tests" in data
    assert "passed_tests" in data
    assert "failed_tests" in data
    assert "pass_rate" in data
    assert "security_scans" in data
    assert "regression_history" in data


def test_find_batch_metrics():
    report = {
        "summary": {
            "total_tests": 10,
            "passed": 8,
            "failed": 2
        }
    }

    result = find_metrics(report)

    assert result["total_tests"] == 10
    assert result["passed"] == 8
    assert result["failed"] == 2


def test_find_reliability_metrics():
    report = {
        "results": {
            "total_requests": 10,
            "successful_requests": 9,
            "failed_requests": 1,
            "average_latency_ms": 120
        }
    }

    result = find_metrics(report)

    assert result["total_tests"] == 10
    assert result["passed"] == 9
    assert result["failed"] == 1
    assert result["average_latency_ms"] == 120


def test_find_metrics_returns_none_for_unknown_report():
    result = find_metrics({"message": "No metrics available"})

    assert result is None