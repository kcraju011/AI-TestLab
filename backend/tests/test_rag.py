import pytest

from app.rag.chunker import split_text
from app.core.paths import BACKEND_DIR
from app.models.rag_schemas import RAGRequest
from app.services.rag_service import DOCUMENTS_DIR, RAGService


def test_split_text_creates_chunks():

    text = " ".join(
        [f"word{i}" for i in range(250)]
    )

    chunks = split_text(
        text,
        chunk_size=100,
        overlap=20
    )

    assert len(chunks) == 3


def test_chunks_contain_expected_words():

    text = "one two three four five six"

    chunks = split_text(
        text,
        chunk_size=4,
        overlap=2
    )

    assert chunks[0] == "one two three four"
    assert chunks[1] == "three four five six"


def test_empty_text_returns_empty_list():

    assert split_text("") == []


def test_invalid_chunk_size():

    with pytest.raises(ValueError):
        split_text(
            "hello world",
            chunk_size=0,
            overlap=0
        )


def test_overlap_must_be_smaller_than_chunk_size():

    with pytest.raises(ValueError):
        split_text(
            "hello world",
            chunk_size=5,
            overlap=5
        )


def test_rag_documents_path_resolves_inside_backend():
    assert DOCUMENTS_DIR == BACKEND_DIR / "app" / "rag" / "documents"


def test_mock_rag_answer_uses_retrieved_context_without_api_key(monkeypatch):
    from app.core import config

    monkeypatch.setattr(config.settings, "OPENAI_API_KEY", None)
    service = RAGService.__new__(RAGService)
    service.retrieve = lambda question, top_k: [
        "Employees receive 20 annual paid leave days per calendar year."
    ]

    result = service.ask(
        question="How many annual paid leave days are provided?",
        provider="mock"
    )

    assert result["provider"] == "mock"
    assert result["retrieved_chunks"] == 1
    assert "20 annual paid leave days" in result["answer"]


def test_rag_request_accepts_mock_provider():
    request = RAGRequest(question="What is the leave policy?", provider="mock")

    assert request.provider == "mock"