from fastapi import APIRouter, HTTPException

from app.models.reliability_schemas import (
    ReliabilityRequest,
    ReliabilityResponse
)
from app.reliability.reliability_report import ReliabilityReport


router = APIRouter(
    prefix="/api/v1/reliability",
    tags=["Reliability Testing"]
)

report_service = ReliabilityReport()


@router.post("/run", response_model=ReliabilityResponse)
def run_reliability_test(request: ReliabilityRequest):

    try:
        report = report_service.generate(
            total_requests=request.total_requests,
            simulated_delay_ms=request.simulated_delay_ms,
            failure_every=request.failure_every
        )

        return report["results"]

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Reliability test could not be completed"
        ) from error