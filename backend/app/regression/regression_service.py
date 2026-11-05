from uuid import uuid4

from sqlalchemy.orm import Session

from app.database.database_service import DatabaseService
from app.database.schemas import (
    TestRunCreate,
    TestCaseResultCreate,
)
from app.regression.schemas import (
    RegressionRequest,
    RegressionResponse,
)
from app.regression.regression_engine import RegressionEngine


def compare_and_save(
    db: Session,
    request: RegressionRequest,
) -> RegressionResponse:

    result = RegressionEngine.compare(request)

    run_id = str(uuid4())
    result.run_id = run_id

    case_results = []

    for comparison in result.comparisons:

        case_status = (
            "FAIL"
            if comparison.is_regression
            else "PASS"
        )

        case_results.append(
            TestCaseResultCreate(
                test_id=comparison.test_id,
                status=case_status,
                details=comparison.model_dump(),
            )
        )

    passed = result.total_compared - result.regression_count
    failed = result.regression_count

    database_payload = TestRunCreate(
        module="regression",
        source_run_id=run_id,
        total_tests=result.total_compared,
        passed=passed,
        failed=failed,
        pass_rate=round(
            (passed / result.total_compared) * 100,
            2,
        ),
        average_latency_ms=0,
        status="FAIL" if failed else "PASS",
        results=case_results,
    )

    DatabaseService.create_run(db, database_payload)

    return result