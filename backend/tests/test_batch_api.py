import json

from fastapi.testclient import TestClient

from app.main import app
from app.services import batch_runner as batch_module


client = TestClient(app)


def test_batch_run_with_mock_provider():
    response = client.post(
        "/api/v1/batches/run",
        json={"provider": "mock"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["summary"]["total_tests"] == 5
    assert data["summary"]["passed"] == 3
    assert data["summary"]["failed"] == 2
    assert len(data["results"]) == 5


def test_batch_results_contain_test_ids():
    response = client.post(
        "/api/v1/batches/run",
        json={"provider": "mock"}
    )

    data = response.json()

    test_ids = [
        result["test_id"]
        for result in data["results"]
    ]

    assert test_ids == [
        "TC001",
        "TC002",
        "TC003",
        "TC004",
        "TC005"
    ]


def test_batch_report_is_saved(tmp_path, monkeypatch):
    report_dir = tmp_path / "reports"

    monkeypatch.setattr(
        batch_module,
        "REPORTS_DIR",
        report_dir
    )

    response = client.post(
        "/api/v1/batches/run",
        json={"provider": "mock"}
    )

    assert response.status_code == 200

    data = response.json()

    report_path = report_dir / f"batch_{data['batch_id']}.json"

    assert report_path.exists()

    with open(report_path, "r", encoding="utf-8") as file:
        report = json.load(file)

    assert report["batch_id"] == data["batch_id"]
    assert report["summary"]["total_tests"] == 5


def test_invalid_provider_is_rejected():
    response = client.post(
        "/api/v1/batches/run",
        json={"provider": "unknown"}
    )

    assert response.status_code == 422


def test_batch_summary_values():
    response = client.post(
        "/api/v1/batches/run",
        json={"provider": "mock"}
    )

    summary = response.json()["summary"]

    assert summary["total_tests"] == (
        summary["passed"] + summary["failed"]
    )

    assert 0 <= summary["pass_rate"] <= 100
    assert 0 <= summary["average_score"] <= 1