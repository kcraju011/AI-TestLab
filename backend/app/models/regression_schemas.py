from typing import List

from pydantic import BaseModel, Field


class RegressionRequest(BaseModel):
    suite_name: str = Field(min_length=1, max_length=100)


class RegressionSummary(BaseModel):
    run_id: str
    suite_name: str
    total_tests: int
    passed: int
    failed: int
    pass_rate: float
    regression_count: int
    regressions: List[str]
    status: str