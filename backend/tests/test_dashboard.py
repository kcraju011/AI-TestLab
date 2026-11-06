import json
import os
import time

from fastapi.testclient import TestClient

from app.main import app
from app.dashboard import dashboard_service
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


def test_dashboard_allows_vite_port_5174():
    response = client.get(
        "/api/v1/dashboard/summary",
        headers={"Origin": "http://localhost:5174"},
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5174"


def test_dashboard_allows_docker_frontend_port_8081():
    response = client.get(
        "/api/v1/dashboard/summary",
        headers={"Origin": "http://localhost:8081"},
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:8081"


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


def test_dashboard_summary_reads_batch_reports(tmp_path, monkeypatch):
    report = {
        "batch_id": "test-batch",
        "summary": {
            "total_tests": 5,
            "passed": 3,
            "failed": 2
        }
    }
    (tmp_path / "batch_test-batch.json").write_text(
        json.dumps(report),
        encoding="utf-8"
    )
    monkeypatch.setattr(dashboard_service, "REPORTS_DIR", tmp_path)

    summary = dashboard_service.DashboardService().get_summary()

    assert summary["total_tests"] == 5
    assert summary["passed_tests"] == 3
    assert summary["failed_tests"] == 2
    assert summary["recent_runs"][0]["file"] == "batch_test-batch.json"


def test_dashboard_shows_new_batch_ahead_of_older_reports(
    tmp_path,
    monkeypatch
):
    old_report = {
        "results": {
            "total_requests": 1,
            "successful_requests": 1,
            "failed_requests": 0
        }
    }
    old_time = time.time() - 60
    for index in range(12):
        path = tmp_path / f"reliability_old-{index}.json"
        path.write_text(json.dumps(old_report), encoding="utf-8")
        os.utime(path, (old_time, old_time))

    batch_path = tmp_path / "batch_new.json"
    batch_path.write_text(
        json.dumps({
            "summary": {
                "total_tests": 5,
                "passed": 3,
                "failed": 2
            }
        }),
        encoding="utf-8"
    )
    monkeypatch.setattr(dashboard_service, "REPORTS_DIR", tmp_path)

    summary = dashboard_service.DashboardService().get_summary()

    assert summary["recent_runs"][0]["file"] == "batch_new.json"
    assert len(summary["recent_runs"]) == 10