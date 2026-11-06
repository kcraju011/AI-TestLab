import json
from pathlib import Path

from app.regression.regression_engine import RegressionEngine
from app.regression.test_suites import TEST_SUITES
from app.core.paths import BACKEND_DIR


DEFAULT_REPORT_DIR = BACKEND_DIR / "reports" / "regression"


class RegressionReport:

    def __init__(self, report_dir: Path = DEFAULT_REPORT_DIR):
        self.report_dir = Path(report_dir)
        self.report_dir.mkdir(parents=True, exist_ok=True)
        self.engine = RegressionEngine()

    def _history_file(self, suite_name: str) -> Path:
        return self.report_dir / f"{suite_name}_history.json"

    def _load_history(self, suite_name: str) -> list:
        history_file = self._history_file(suite_name)

        if not history_file.exists():
            return []

        with open(history_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def run(self, suite_name: str) -> dict:

        if suite_name not in TEST_SUITES:
            raise ValueError(f"Unknown test suite: {suite_name}")

        history = self._load_history(suite_name)

        current_run = self.engine.run_suite(
            suite_name,
            TEST_SUITES[suite_name]
        )

        regressions = []

        if history:
            previous_run = history[-1]
            regressions = self.engine.detect_regressions(
                previous_run,
                current_run
            )

        current_run["regressions"] = regressions
        current_run["regression_count"] = len(regressions)

        current_run["status"] = (
            "FAIL"
            if current_run["failed"] > 0 or regressions
            else "PASS"
        )

        history.append(current_run)

        with open(
            self._history_file(suite_name),
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(history, file, indent=4)

        return current_run