from typing import List, Literal, Optional

from pydantic import BaseModel, Field, ConfigDict


class ModelTestCase(BaseModel):
    test_id: str = Field(min_length=1)
    score: float = Field(ge=0, le=1)
    status: Literal["PASS", "FAIL"]


class ModelEvaluation(BaseModel):
    model_name: str = Field(min_length=1)
    model_version: str = Field(min_length=1)
    test_cases: List[ModelTestCase] = Field(min_length=1)


class RegressionRequest(BaseModel):
    baseline: ModelEvaluation
    candidate: ModelEvaluation

    # A score decrease greater than this is a regression.
    score_drop_threshold: float = Field(
        default=0.10,
        ge=0,
        le=1,
    )


class TestCaseComparison(BaseModel):
    test_id: str
    baseline_score: float
    candidate_score: float
    score_change: float
    baseline_status: str
    candidate_status: str
    is_regression: bool


class RegressionResponse(BaseModel):
    run_id: str
    baseline_model: str
    candidate_model: str
    baseline_average_score: float
    candidate_average_score: float
    score_change: float
    regression_count: int
    improved_count: int
    unchanged_count: int
    total_compared: int
    regression_rate: float
    status: str
    comparisons: List[TestCaseComparison]


class RegressionHistoryItem(BaseModel):
    id: int
    module: str
    source_run_id: Optional[str] = None
    total_tests: int
    passed: int
    failed: int
    pass_rate: float
    status: str

    model_config = ConfigDict(from_attributes=True)