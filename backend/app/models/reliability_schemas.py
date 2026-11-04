from pydantic import BaseModel, Field


class ReliabilityRequest(BaseModel):
    total_requests: int = Field(default=10, ge=1, le=500)
    simulated_delay_ms: int = Field(default=100, ge=0, le=10000)
    failure_every: int = Field(default=0, ge=0)


class ReliabilityResponse(BaseModel):
    total_requests: int
    successful_requests: int
    failed_requests: int
    success_rate: float
    average_latency_ms: float
    min_latency_ms: float
    max_latency_ms: float
    p95_latency_ms: float
    status: str