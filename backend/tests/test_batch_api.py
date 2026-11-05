import json
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import batch_persistence
from app.database.schemas import TestRunCreate
from app.routes import batch_routes
from app.services import batch_runner as batch_module


client = TestClient(app)


@pytest.fixture(autouse=True)
def mock_batch_database_save(monkeypatch):
    monkeypatch.setattr(
        batch_routes,
        "save_batch_result",
        lambda db, result: SimpleNamespace(id=123)
    )


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
    assert data["database_run_id"] == 123


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


def test_batch_persistence_maps_completed_batch(monkeypatch):
    captured = {}

    def fake_create_run(db, payload):
        captured["db"] = db
        captured["payload"] = payload
        return SimpleNamespace(id=456)

    monkeypatch.setattr(
        batch_persistence.DatabaseService,
        "create_run",
        fake_create_run
    )

    batch_result = {
        "batch_id": "batch-123",
        "provider": "mock",
        "summary": {
            "total_tests": 2,
            "passed": 1,
            "failed": 1,
            "pass_rate": 50.0,
            "average_score": 0.5
        },
        "results": [
            {
                "test_id": "TC001",
                "status": "PASS",
                "execution_time_ms": 10.0,
            },
            {
                "test_id": "TC002",
                "status": "FAIL",
                "execution_time_ms": 20.0,
            },
        ]
    }

    saved_run = batch_persistence.save_batch_result(
        db="session",
        batch_result=batch_result
    )

    payload = captured["payload"]
    assert saved_run.id == 456
    assert captured["db"] == "session"
    assert isinstance(payload, TestRunCreate)
    assert payload.source_run_id == "batch-123"
    assert payload.total_tests == 2
    assert payload.passed == 1
    assert payload.failed == 1
    assert payload.pass_rate == 50.0
    assert payload.average_latency_ms == 15.0
    assert [item.status for item in payload.results] == ["PASS", "FAIL"]