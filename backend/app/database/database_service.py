from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database.models import TestRun, TestCaseResult
from app.database.schemas import TestRunCreate


class DatabaseService:

    @staticmethod
    def create_run(
        db: Session,
        payload: TestRunCreate
    ) -> TestRun:

        if payload.passed + payload.failed > payload.total_tests:
            raise ValueError(
                "Passed plus failed cannot exceed total tests"
            )

        if payload.results and len(payload.results) != payload.total_tests:
            raise ValueError(
                "Number of individual results must equal total_tests"
            )

        if payload.results:
            actual_passed = sum(
                result.status == "PASS"
                for result in payload.results
            )
            actual_failed = sum(
                result.status in ("FAIL", "ERROR")
                for result in payload.results
            )

            if (
                actual_passed != payload.passed
                or actual_failed != payload.failed
            ):
                raise ValueError(
                    "Individual results do not match run summary"
                )

        run = TestRun(
            module=payload.module,
            source_run_id=payload.source_run_id,
            total_tests=payload.total_tests,
            passed=payload.passed,
            failed=payload.failed,
            pass_rate=payload.pass_rate,
            average_latency_ms=payload.average_latency_ms,
            status=payload.status
        )

        run.results = [
            TestCaseResult(
                test_id=item.test_id,
                status=item.status,
                details=item.details
            )
            for item in payload.results
        ]

        try:
            db.add(run)
            db.commit()
            db.refresh(run)
            return run

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_run(db: Session, run_id: int):
        statement = (
            select(TestRun)
            .options(selectinload(TestRun.results))
            .where(TestRun.id == run_id)
        )

        return db.scalars(statement).first()

    @staticmethod
    def get_history(
        db: Session,
        module: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> List[TestRun]:

        statement = select(TestRun).order_by(
            TestRun.created_at.desc(),
            TestRun.id.desc()
        )

        if module:
            statement = statement.where(TestRun.module == module)

        statement = statement.offset(offset).limit(limit)

        return list(db.scalars(statement).all())