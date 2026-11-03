from fastapi.testclient import TestClient

from app.main import app
import app.routes.test_routes as test_routes


client = TestClient(app)


def test_mock_provider():

    payload = {
        "question": "What is the fan warranty?",
        "expected_answer": "This fan has a two year warranty.",
        "scenario": "correct",
        "provider": "mock"
    }

    response = client.post(
        "/api/v1/tests/run",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["provider"] == "mock"
    assert data["status"] == "PASS"


def test_response_contains_latency():

    payload = {
        "question": "What is the fan warranty?",
        "expected_answer": "This fan has a two year warranty.",
        "provider": "mock"
    }

    response = client.post(
        "/api/v1/tests/run",
        json=payload
    )

    assert response.status_code == 200

    assert response.json()["execution_time_ms"] >= 0


def test_response_contains_token_metadata():

    payload = {
        "question": "What is the fan warranty?",
        "expected_answer": "This fan has a two year warranty.",
        "provider": "mock"
    }

    response = client.post(
        "/api/v1/tests/run",
        json=payload
    )

    data = response.json()

    assert data["input_tokens"] == 0
    assert data["output_tokens"] == 0
    assert data["model"] == "mock-model"


def test_openai_provider_failure(monkeypatch):

    def fake_openai_service():
        raise test_routes.LLMProviderError(
            "LLM connection or timeout failure"
        )

    monkeypatch.setattr(
        test_routes,
        "OpenAILLMService",
        fake_openai_service
    )

    payload = {
        "question": "What is the fan warranty?",
        "expected_answer": "This fan has a two year warranty.",
        "provider": "openai"
    }

    response = client.post(
        "/api/v1/tests/run",
        json=payload
    )

    assert response.status_code == 502

    assert "timeout" in response.json()["detail"]


def test_invalid_provider():

    payload = {
        "question": "What is the fan warranty?",
        "expected_answer": "This fan has a two year warranty.",
        "provider": "gemini"
    }

    response = client.post(
        "/api/v1/tests/run",
        json=payload
    )

    assert response.status_code == 422
