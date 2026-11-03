from typing import Literal

from pydantic import BaseModel, Field


class TestRequest(BaseModel):

    question: str = Field(
        min_length=3,
        max_length=500
    )

    expected_answer: str = Field(
        min_length=1,
        max_length=1000
    )

    scenario: Literal[
        "correct",
        "incorrect",
        "empty"
    ] = "correct"

    provider: Literal[
        "mock",
        "openai"
    ] = "mock"


class TestResponse(BaseModel):

    test_id: str
    question: str
    expected_answer: str
    actual_answer: str

    score: float
    status: str

    execution_time_ms: float

    provider: str
    model: str

    input_tokens: int
    output_tokens: int

    message: str