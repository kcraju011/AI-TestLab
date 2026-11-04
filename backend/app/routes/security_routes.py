from fastapi import APIRouter, HTTPException

from app.models.security_schemas import (
    SecurityScanRequest,
    SecurityScanResponse,
    SecurityBatchResponse
)

from app.evaluators.security_evaluator import SecurityEvaluator
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


@router.post("/evaluate-pii")
def evaluate_pii(request: SecurityScanRequest):

    try:

        evaluator = SecurityEvaluator()

        result = evaluator.evaluate_pii(
            prompt=request.prompt,
            actual_output=request.response
        )

        return result

    except Exception as error:

        raise HTTPException(
            status_code=502,
            detail=f"PII evaluation failed: {str(error)}"
        )
