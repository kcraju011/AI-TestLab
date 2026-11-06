from typing import List, Literal

from pydantic import BaseModel, Field


class IngestResponse(BaseModel):
    documents_processed: int
    chunks_created: int
    sources: List[str]


class RAGRequest(BaseModel):
    question: str = Field(
        min_length=3,
        max_length=1000
    )

    top_k: int = Field(
        default=3,
        ge=1,
        le=10
    )

    provider: Literal["mock", "openai"] = "openai"


class RAGResponse(BaseModel):
    question: str
    answer: str
    retrieved_context: List[str]
    retrieved_chunks: int
    provider: Literal["mock", "openai"]


class RAGEvaluationRequest(BaseModel):
    question: str = Field(min_length=3)
    actual_answer: str = Field(min_length=1)
    expected_answer: str = Field(min_length=1)
    retrieval_context: List[str] = Field(min_length=1)