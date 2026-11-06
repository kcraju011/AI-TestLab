import json
import uuid

from app.security.attack_dataset import SECURITY_TEST_CASES
from app.security.security_engine import SecurityEngine
from app.core.paths import BACKEND_DIR


REPORTS_DIR = BACKEND_DIR / "reports"


class SecurityReportService:

    def __init__(self):
        self.engine = SecurityEngine()

    def run_tests(self):

        results = []

        for test_case in SECURITY_TEST_CASES:

            result = self.engine.evaluate(
                prompt=test_case["prompt"],
                response="This is a safe simulated response."
            )

            actual_detection = (
                result["input_security"]["detected"]
            )

            expected_detection = (
                test_case["expected_detection"]
            )

            test_passed = (
                actual_detection == expected_detection
            )

            results.append({
                "test_id": test_case["test_id"],
                "category": test_case["category"],
                "expected_detection": expected_detection,
                "actual_detection": actual_detection,
                "test_status": (
                    "PASS" if test_passed else "FAIL"
                ),
                "security_result": result
            })

        total = len(results)

        passed = sum(
            1 for item in results
            if item["test_status"] == "PASS"
        )

        failed = total - passed

        summary = {
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": round(
                (passed / total) * 100 if total else 0,
                2
            )
        }

        batch_id = str(uuid.uuid4())

        report = {
            "batch_id": batch_id,
            "summary": summary,
            "results": results
        }

        REPORTS_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        report_path = (
            REPORTS_DIR / f"security_{batch_id}.json"
        )

        with open(
            report_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                report,
                file,
                indent=4
            )

        return {
            **report,
            **summary,
            "report_file": str(report_path)
        }