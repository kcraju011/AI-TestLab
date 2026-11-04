from fastapi import APIRouter, HTTPException

from app.models.security_schemas import (
    SecurityScanRequest,
    SecurityScanResponse,
    SecurityBatchResponse
)

from app.security.security_engine import SecurityEngine
from app.services.security_report import SecurityReportService


router = APIRouter(
    prefix="/api/v1/security",
    tags=["AI Security Testing"]
)


@router.post(
    "/scan",
    response_model=SecurityScanResponse
)
def scan_security(request: SecurityScanRequest):

    try:

        engine = SecurityEngine()

        result = engine.evaluate(
            prompt=request.prompt,
            response=request.response
        )

        return result

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Security scan failed: {str(error)}"
        )


@router.post(
    "/run-tests",
    response_model=SecurityBatchResponse
)
def run_security_tests():

    try:

        service = SecurityReportService()

        return service.run_tests()

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Security testing failed: {str(error)}"
        )