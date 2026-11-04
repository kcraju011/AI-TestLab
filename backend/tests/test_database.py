import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database.session import Base, get_db


TEST_ENGINE = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    bind=TEST_ENGINE,
    autoflush=False,
    expire_on_commit=False
)


@pytest.fixture
def client():
    Base.metadata.create_all(bind=TEST_ENGINE)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=TEST_ENGINE)


def sample_payload():
    return {
        "module": "batch",
        "source_run_id": "test-001",
        "total_tests": 2,
        "passed": 1,
        "failed": 1,
        "pass_rate": 50,
        "average_latency_ms": 100,
        "status": "FAIL",
        "results": [
            {
                "test_id": "QA001",
                "status": "PASS",
                "details": {"message": "Passed"}
            },
            {
                "test_id": "QA002",
                "status": "FAIL",
                "details": {"message": "Failed"}
            }
        ]
    }


def test_save_test_run(client):
    response = client.post(
        "/api/v1/database/runs",
        json=sample_payload()
    )

    assert response.status_code == 201
    assert response.json()["total_tests"] == 2
    assert response.json()["failed"] == 1


def test_get_test_history(client):
    client.post(
        "/api/v1/database/runs",
        json=sample_payload()
    )

    response = client.get("/api/v1/database/runs")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_filter_test_history(client):
    client.post(
        "/api/v1/database/runs",
        json=sample_payload()
    )

    response = client.get(
        "/api/v1/database/runs?module=batch"
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_individual_test_cases(client):
    saved = client.post(
        "/api/v1/database/runs",
        json=sample_payload()
    )

    run_id = saved.json()["id"]

    response = client.get(
        f"/api/v1/database/runs/{run_id}/cases"
    )

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_unknown_run_returns_404(client):
    response = client.get("/api/v1/database/runs/99999")

    assert response.status_code == 404


def test_invalid_summary_rejected(client):
    payload = sample_payload()
    payload["passed"] = 5

    response = client.post(
        "/api/v1/database/runs",
        json=payload
    )

    assert response.status_code == 422


def test_results_must_match_summary(client):
    payload = sample_payload()
    payload["results"] = payload["results"][:1]

    response = client.post(
        "/api/v1/database/runs",
        json=payload
    )

    assert response.status_code == 422