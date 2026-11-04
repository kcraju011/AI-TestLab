from fastapi import APIRouter, HTTPException

from app.models.regression_schemas import (
    RegressionRequest,
    RegressionSummary
)
from app.regression.test_suites import TEST_SUITES
from app.regression.regression_report import RegressionReport


router = APIRouter(
    prefix="/api/v1/regression",
    tags=["Regression Testing"]
)

report_service = RegressionReport()


@router.get("/suites")
def list_suites():
    return {
        "suites": [
            {
                "suite_name": name,
                "test_count": len(test_cases)
            }
            for name, test_cases in TEST_SUITES.items()
        ]
    }


@router.post("/run", response_model=RegressionSummary)
def run_regression(request: RegressionRequest):

    try:
        result = report_service.run(request.suite_name)

        return {
            "run_id": result["run_id"],
            "suite_name": result["suite_name"],
            "total_tests": result["total_tests"],
            "passed": result["passed"],
            "failed": result["failed"],
            "pass_rate": result["pass_rate"],
            "regression_count": result["regression_count"],
            "regressions": result["regressions"],
            "status": result["status"]
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Regression test execution failed"
        ) from error