from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class BatchRunRequest(BaseModel):
    provider: Literal["mock", "openai"] = "mock"


class BatchTestResult(BaseModel):
    test_id: str
    category: str
    question: str
    expected_answer: str
    actual_answer: str
    score: float
    status: str
    execution_time_ms: float
    provider: str
    model: Optional[str] = None


class BatchSummary(BaseModel):
    total_tests: int
    passed: int
    failed: int
    average_score: float
    pass_rate: float


class BatchRunResponse(BaseModel):
    batch_id: str
    provider: str
    summary: BatchSummary
    results: List[BatchTestResult]
    report_file: str