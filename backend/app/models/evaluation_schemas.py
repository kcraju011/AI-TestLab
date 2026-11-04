from typing import List, Optional

from pydantic import BaseModel, Field


class EvaluationRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1000)

    actual_answer: str = Field(
        min_length=1,
        max_length=5000
    )

    context: List[str] = Field(
        min_length=1,
        description="Trusted reference context for hallucination evaluation"
    )

    retrieval_context: List[str] = Field(
        min_length=1,
        description="Retrieved context for faithfulness evaluation"
    )


class MetricResult(BaseModel):
    score: float
    threshold: float
    passed: bool
    reason: Optional[str] = None


class EvaluationResponse(BaseModel):
    question: str
    actual_answer: str
    answer_relevancy: MetricResult
    faithfulness: MetricResult
    hallucination: MetricResult
    overall_status: str