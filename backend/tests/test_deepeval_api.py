from fastapi.testclient import TestClient

from app.main import app
from app.routes import evaluation_routes


client = TestClient(app)


def fake_evaluation(
    question,
    actual_answer,
    context,
    retrieval_context
):
    metric = {
        "score": 0.95,
        "threshold": 0.70,
        "passed": True,
        "reason": "Mock evaluation passed."
    }

    return {
        "answer_relevancy": metric,
        "faithfulness": metric,
        "hallucination": metric,
        "overall_status": "PASS"
    }


def test_evaluation_endpoint(monkeypatch):

    monkeypatch.setattr(
        evaluation_routes.DeepEvalEvaluator,
        "evaluate",
        lambda self, **kwargs: fake_evaluation(**kwargs)
    )

    response = client.post(
        "/api/v1/evaluations/run",
        json={
            "question": "What is Python?",
            "actual_answer": "Python is a programming language.",
            "context": [
                "Python is a high-level programming language."
            ],
            "retrieval_context": [
                "Python is a high-level programming language."
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["overall_status"] == "PASS"
    assert data["answer_relevancy"]["score"] == 0.95
    assert data["faithfulness"]["passed"] is True
    assert data["hallucination"]["passed"] is True


def test_missing_context_is_rejected():

    response = client.post(
        "/api/v1/evaluations/run",
        json={
            "question": "What is Python?",
            "actual_answer": "Python is a programming language.",
            "context": [],
            "retrieval_context": []
        }
    )

    assert response.status_code == 422


def test_missing_actual_answer_is_rejected():

    response = client.post(
        "/api/v1/evaluations/run",
        json={
            "question": "What is Python?",
            "context": ["Python is a programming language."],
            "retrieval_context": [
                "Python is a programming language."
            ]
        }
    )

    assert response.status_code == 422
    