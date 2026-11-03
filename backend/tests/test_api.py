from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json()["status"] == "healthy"


def test_correct_ai_response():

    payload = {
        "question": "What is the fan warranty?",
        "expected_answer": "This fan has a two year warranty.",
        "scenario": "correct"
    }

    response = client.post(
        "/api/v1/tests/run",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "PASS"

    assert data["score"] == 1.0


def test_incorrect_ai_response():

    payload = {
        "question": "What is the fan warranty?",
        "expected_answer": "This fan has a two year warranty.",
        "scenario": "incorrect"
    }

    response = client.post(
        "/api/v1/tests/run",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "FAIL"

    assert data["score"] < 0.70


def test_empty_ai_response():

    payload = {
        "question": "What is the fan warranty?",
        "expected_answer": "This fan has a two year warranty.",
        "scenario": "empty"
    }

    response = client.post(
        "/api/v1/tests/run",
        json=payload
    )

    assert response.status_code == 200

    assert response.json()["status"] == "FAIL"


def test_invalid_question():

    payload = {
        "question": "Hi",
        "expected_answer": "Warranty is two years.",
        "scenario": "correct"
    }

    response = client.post(
        "/api/v1/tests/run",
        json=payload
    )

    assert response.status_code == 422