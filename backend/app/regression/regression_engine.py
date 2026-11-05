from app.regression.schemas import (
    RegressionRequest,
    RegressionResponse,
    TestCaseComparison,
)


class RegressionEngine:

    @staticmethod
    def compare(request: RegressionRequest) -> RegressionResponse:

        baseline_cases = {
            case.test_id: case
            for case in request.baseline.test_cases
        }

        candidate_cases = {
            case.test_id: case
            for case in request.candidate.test_cases
        }

        # Compare only test IDs present in both evaluations.
        common_ids = sorted(
            set(baseline_cases) & set(candidate_cases)
        )

        if not common_ids:
            raise ValueError(
                "Baseline and candidate have no matching test IDs"
            )

        comparisons = []

        regression_count = 0
        improved_count = 0
        unchanged_count = 0

        for test_id in common_ids:

            old = baseline_cases[test_id]
            new = candidate_cases[test_id]

            score_change = round(
                new.score - old.score,
                4,
            )

            # A PASS-to-FAIL transition is always a regression.
            failed_transition = (
                old.status == "PASS"
                and new.status == "FAIL"
            )

            # Also detect a significant numerical score decrease.
            score_regression = (
                score_change < -request.score_drop_threshold
            )

            is_regression = (
                failed_transition or score_regression
            )

            if is_regression:
                regression_count += 1

            elif score_change > 0:
                improved_count += 1

            else:
                unchanged_count += 1

            comparisons.append(
                TestCaseComparison(
                    test_id=test_id,
                    baseline_score=old.score,
                    candidate_score=new.score,
                    score_change=score_change,
                    baseline_status=old.status,
                    candidate_status=new.status,
                    is_regression=is_regression,
                )
            )

        baseline_average = sum(
            baseline_cases[test_id].score
            for test_id in common_ids
        ) / len(common_ids)

        candidate_average = sum(
            candidate_cases[test_id].score
            for test_id in common_ids
        ) / len(common_ids)

        score_change = candidate_average - baseline_average

        regression_rate = (
            regression_count / len(common_ids)
        ) * 100

        status = (
            "REGRESSION"
            if regression_count > 0
            else "PASS"
        )

        return RegressionResponse(
            run_id="pending",
            baseline_model=(
                f"{request.baseline.model_name}:"
                f"{request.baseline.model_version}"
            ),
            candidate_model=(
                f"{request.candidate.model_name}:"
                f"{request.candidate.model_version}"
            ),
            baseline_average_score=round(
                baseline_average, 4
            ),
            candidate_average_score=round(
                candidate_average, 4
            ),
            score_change=round(score_change, 4),
            regression_count=regression_count,
            improved_count=improved_count,
            unchanged_count=unchanged_count,
            total_compared=len(common_ids),
            regression_rate=round(regression_rate, 2),
            status=status,
            comparisons=comparisons,
        )