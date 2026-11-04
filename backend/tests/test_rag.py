import pytest

from app.rag.chunker import split_text


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