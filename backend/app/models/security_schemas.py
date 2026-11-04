from typing import Dict, List

from pydantic import BaseModel, Field


class SecurityScanRequest(BaseModel):

    prompt: str = Field(
        min_length=1,
        max_length=5000
    )

    response: str = Field(
        min_length=1,
        max_length=10000
    )


class SecurityScanResponse(BaseModel):

    input_security: Dict
    output_security: Dict
    findings: List[Dict]
    risk_score: int
    overall_status: str


class SecurityBatchSummary(BaseModel):
    total_tests: int
    passed: int
    failed: int
    pass_rate: float


class SecurityBatchResponse(BaseModel):
    batch_id: str
    summary: SecurityBatchSummary
    total_tests: int
    passed: int
    failed: int
    pass_rate: float
    results: List[Dict]
    report_file: str