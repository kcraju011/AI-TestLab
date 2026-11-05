import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.batch_persistence import save_batch_result
from app.database.session import Base


@pytest.fixture
def db_session():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(bind=engine)
    test_session = sessionmaker(bind=engine)()

    try:
        yield test_session
    finally:
        test_session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_save_batch_result(db_session):
    batch_result = {
        "run_id": "day12-test-001",
        "total_tests": 2,
        "passed": 1,
        "failed": 1,
        "pass_rate": 50.0,
        "average_latency_ms": 100.0,
        "results": [
            {
                "test_id": "TC001",
                "status": "PASS",
                "score": 0.95,
            },
            {
                "test_id": "TC002",
                "status": "FAIL",
                "score": 0.25,
            },
        ],
    }

    saved = save_batch_result(db_session, batch_result)

    assert saved.id is not None
    assert saved.total_tests == 2
    assert saved.passed == 1
    assert saved.failed == 1
    assert len(saved.results) == 2