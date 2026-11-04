from datetime import datetime, timezone
from uuid import uuid4


class RegressionEngine:

    @staticmethod
    def normalize(text: str) -> str:
        return " ".join(text.lower().strip().split())

    def evaluate_case(self, test_case: dict) -> dict:
        expected = self.normalize(test_case["expected_answer"])
        actual = self.normalize(test_case["actual_answer"])

        passed = expected == actual

        return {
            "test_id": test_case["test_id"],
            "question": test_case["question"],
            "passed": passed,
            "expected_answer": test_case["expected_answer"],
            "actual_answer": test_case["actual_answer"],
            "status": "PASS" if passed else "FAIL"
        }

    def run_suite(self, suite_name: str, test_cases: list) -> dict:

        results = [
            self.evaluate_case(test_case)
            for test_case in test_cases
        ]

        total = len(results)
        passed = sum(1 for item in results if item["passed"])
        failed = total - passed

        pass_rate = (passed / total * 100) if total else 0.0

        return {
            "run_id": str(uuid4()),
            "suite_name": suite_name,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": round(pass_rate, 2),
            "results": results
        }

    @staticmethod
    def detect_regressions(previous_run: dict, current_run: dict) -> list:

        previous_results = {
            item["test_id"]: item["passed"]
            for item in previous_run["results"]
        }

        regressions = []

        for current in current_run["results"]:
            test_id = current["test_id"]

            if (
                previous_results.get(test_id) is True
                and current["passed"] is False
            ):
                regressions.append(test_id)

        return regressions