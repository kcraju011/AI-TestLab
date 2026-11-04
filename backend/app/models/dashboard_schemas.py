from typing import Dict, List

from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_tests: int
    passed_tests: int
    failed_tests: int
    pass_rate: float
    security_scans: int
    security_findings: int
    reliability_runs: int
    average_latency_ms: float
    regression_runs: int
    regression_count: int
    recent_runs: List[Dict]
    regression_history: List[Dict]
    data_notes: List[str]