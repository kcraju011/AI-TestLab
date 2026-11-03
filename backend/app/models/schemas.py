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

    scenario: str = Field(
        default="correct",
        pattern="^(correct|incorrect|empty)$"
    )


class TestResponse(BaseModel):
    test_id: str
    question: str
    expected_answer: str
    actual_answer: str
    score: float
    status: str
    execution_time_ms: float
    message: str