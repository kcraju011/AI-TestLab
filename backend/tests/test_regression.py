import pytest

from app.regression.schemas import (
    ModelTestCase,
    ModelEvaluation,
    RegressionRequest,
)
from app.regression.regression_engine import RegressionEngine


def make_request(baseline, candidate, threshold=0.10):

    return RegressionRequest(
        baseline=ModelEvaluation(
            model_name="AI-TestLab",
            model_version="v1",
            test_cases=[
                ModelTestCase(**case)
                for case in baseline
            ],
        ),
        candidate=ModelEvaluation(
            model_name="AI-TestLab",
            model_version="v2",
            test_cases=[
                ModelTestCase(**case)
                for case in candidate
            ],
        ),
        score_drop_threshold=threshold,
    )


def test_detect_score_regression():

    request = make_request(
        baseline=[
            {"test_id": "TC001", "score": 0.95, "status": "PASS"},
        ],
        candidate=[
            {"test_id": "TC001", "score": 0.60, "status": "PASS"},
        ],
    )

    result = RegressionEngine.compare(request)

    assert result.regression_count == 1
    assert result.status == "REGRESSION"
    assert result.score_change == -0.35


def test_detect_pass_to_fail():

    request = make_request(
        baseline=[
            {"test_id": "TC001", "score": 0.90, "status": "PASS"},
        ],
        candidate=[
            {"test_id": "TC001", "score": 0.85, "status": "FAIL"},
        ],
    )

    result = RegressionEngine.compare(request)

    assert result.regression_count == 1


def test_detect_improvement():

    request = make_request(
        baseline=[
            {"test_id": "TC001", "score": 0.60, "status": "PASS"},
        ],
        candidate=[
            {"test_id": "TC001", "score": 0.90, "status": "PASS"},
        ],
    )

    result = RegressionEngine.compare(request)

    assert result.improved_count == 1
    assert result.regression_count == 0
    assert result.status == "PASS"


def test_no_regression_with_small_score_drop():

    request = make_request(
        baseline=[
            {"test_id": "TC001", "score": 0.90, "status": "PASS"},
        ],
        candidate=[
            {"test_id": "TC001", "score": 0.85, "status": "PASS"},
        ],
    )

    result = RegressionEngine.compare(request)

    assert result.regression_count == 0
    assert result.status == "PASS"


def test_no_matching_test_ids():

    request = make_request(
        baseline=[
            {"test_id": "TC001", "score": 0.90, "status": "PASS"},
        ],
        candidate=[
            {"test_id": "TC002", "score": 0.90, "status": "PASS"},
        ],
    )

    with pytest.raises(ValueError):
        RegressionEngine.compare(request)


def test_compare_multiple_test_cases():

    request = make_request(
        baseline=[
            {"test_id": "TC001", "score": 0.90, "status": "PASS"},
            {"test_id": "TC002", "score": 0.70, "status": "PASS"},
            {"test_id": "TC003", "score": 0.80, "status": "PASS"},
        ],
        candidate=[
            {"test_id": "TC001", "score": 0.50, "status": "FAIL"},
            {"test_id": "TC002", "score": 0.90, "status": "PASS"},
            {"test_id": "TC003", "score": 0.80, "status": "PASS"},
        ],
    )

    result = RegressionEngine.compare(request)

    assert result.total_compared == 3
    assert result.regression_count == 1
    assert result.improved_count == 1
    assert result.unchanged_count == 1