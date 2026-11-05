from statistics import mean

from sqlalchemy.orm import Session

from app.database.database_service import DatabaseService
from app.database.schemas import TestRunCreate, TestCaseResultCreate


def save_batch_result(db: Session, batch_result: dict):
    summary = batch_result.get("summary", batch_result)
    results = batch_result.get("results", [])

    total = int(summary["total_tests"])
    passed = int(summary["passed"])
    failed = int(summary["failed"])

    case_results = []

    for item in results:
        status = str(item.get("status", "ERROR")).upper()

        if status not in {"PASS", "FAIL", "ERROR", "SKIPPED"}:
            status = "ERROR"

        case_results.append(
            TestCaseResultCreate(
                test_id=str(item.get("test_id", "UNKNOWN")),
                status=status,
                details=item,
            )
        )

    latencies = [
        float(item["execution_time_ms"])
        for item in results
        if item.get("execution_time_ms") is not None
    ]
    average_latency = (
        mean(latencies)
        if latencies
        else summary.get(
            "average_latency_ms",
            batch_result.get("average_latency_ms")
        )
    )

    payload = TestRunCreate(
        module="batch",
        source_run_id=(
            str(batch_result.get("batch_id") or batch_result.get("run_id", ""))
            or None
        ),
        total_tests=total,
        passed=passed,
        failed=failed,
        pass_rate=float(summary.get("pass_rate", 0)),
        average_latency_ms=(
            float(average_latency)
            if average_latency is not None
            else None
        ),
        status="PASS" if failed == 0 else "FAIL",
        results=case_results,
    )

    return DatabaseService.create_run(db, payload)