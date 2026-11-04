from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, ConfigDict


class TestCaseResultCreate(BaseModel):
    test_id: str = Field(min_length=1, max_length=100)
    status: str = Field(pattern="^(PASS|FAIL|ERROR|SKIPPED)$")
    details: Dict = Field(default_factory=dict)


class TestRunCreate(BaseModel):
    module: str = Field(min_length=1, max_length=100)
    source_run_id: Optional[str] = None

    total_tests: int = Field(ge=0)
    passed: int = Field(ge=0)
    failed: int = Field(ge=0)

    pass_rate: float = Field(ge=0, le=100)
    average_latency_ms: Optional[float] = Field(default=None, ge=0)

    status: str = Field(pattern="^(PASS|FAIL|ERROR|UNKNOWN)$")

    results: List[TestCaseResultCreate] = Field(default_factory=list)


class TestRunResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    module: str
    source_run_id: Optional[str]
    total_tests: int
    passed: int
    failed: int
    pass_rate: float
    average_latency_ms: Optional[float]
    status: str
    created_at: datetime


class TestCaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    run_id: int
    test_id: str
    status: str
    details: Dict