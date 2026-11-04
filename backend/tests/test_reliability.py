from fastapi.testclient import TestClient

from app.main import app
from app.reliability.reliability_engine import ReliabilityEngine


client = TestClient(app)


def test_all_requests_succeed():
    engine = ReliabilityEngine()

    result = engine.run_test(
        total_requests=5,
        simulated_delay_ms=1,
        failure_every=0
    )

    assert result["total_requests"] == 5
    assert result["successful_requests"] == 5
    assert result["failed_requests"] == 0
    assert result["success_rate"] == 100
    assert result["status"] == "PASS"


def test_every_third_request_fails():
    engine = ReliabilityEngine()

    result = engine.run_test(
        total_requests=6,
        simulated_delay_ms=1,
        failure_every=3
    )

    assert result["successful_requests"] == 4
    assert result["failed_requests"] == 2
    assert result["success_rate"] == round((4 / 6) * 100, 2)
    assert result["status"] == "FAIL"


def test_latency_values_are_valid():
    engine = ReliabilityEngine()

    result = engine.run_test(
        total_requests=3,
        simulated_delay_ms=5
    )

    assert result["average_latency_ms"] >= 0
    assert result["min_latency_ms"] >= 0
    assert result["max_latency_ms"] >= result["min_latency_ms"]
    assert result["min_latency_ms"] <= result["p95_latency_ms"]
    assert result["p95_latency_ms"] <= result["max_latency_ms"]


def test_p95_latency_uses_nearest_rank(monkeypatch):
    latency_values = []
    current_time = 0.0
    for request_latency_ms in range(1, 21):
        latency_values.append(current_time)
        current_time += request_latency_ms / 1000
        latency_values.append(current_time)

    times = iter(latency_values)
    monkeypatch.setattr(
        "app.reliability.reliability_engine.time.perf_counter",
        lambda: next(times)
    )
    monkeypatch.setattr(
        "app.reliability.reliability_engine.time.sleep",
        lambda _: None
    )

    result = ReliabilityEngine().run_test(
        total_requests=20,
        simulated_delay_ms=0
    )

    assert result["p95_latency_ms"] == 19.0


def test_reliability_api_success():
    response = client.post(
        "/api/v1/reliability/run",
        json={
            "total_requests": 5,
            "simulated_delay_ms": 1,
            "failure_every": 0
        }
    )

    assert response.status_code == 200
    assert response.json()["success_rate"] == 100
    assert response.json()["status"] == "PASS"
    assert "p95_latency_ms" in response.json()


def test_reliability_api_failure():
    response = client.post(
        "/api/v1/reliability/run",
        json={
            "total_requests": 6,
            "simulated_delay_ms": 1,
            "failure_every": 3
        }
    )

    assert response.status_code == 200
    assert response.json()["failed_requests"] == 2
    assert response.json()["status"] == "FAIL"


def test_invalid_request_rejected():
    response = client.post(
        "/api/v1/reliability/run",
        json={
            "total_requests": 0,
            "simulated_delay_ms": 1
        }
    )

    assert response.status_code == 422