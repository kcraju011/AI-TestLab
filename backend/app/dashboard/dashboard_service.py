import json
from statistics import mean

from app.core.paths import BACKEND_DIR


REPORTS_DIR = BACKEND_DIR / "reports"


def read_json_files(pattern: str) -> list:
    results = []

    for path in REPORTS_DIR.rglob(pattern):
        try:
            with open(path, "r", encoding="utf-8") as file:
                results.append((path, json.load(file)))
        except (OSError, json.JSONDecodeError):
            continue

    return results


def find_metrics(data):
    """Find common test summary fields in a report."""
    if isinstance(data, list):
        for item in data:
            found = find_metrics(item)
            if found:
                return found

    if isinstance(data, dict):
        if all(key in data for key in ("total_tests", "passed", "failed")):
            return data

        if all(key in data for key in (
            "total_requests", "successful_requests", "failed_requests"
        )):
            return {
                "total_tests": data["total_requests"],
                "passed": data["successful_requests"],
                "failed": data["failed_requests"],
                "pass_rate": data.get("success_rate", 0),
                "average_latency_ms": data.get("average_latency_ms", 0)
            }

        for value in data.values():
            found = find_metrics(value)
            if found:
                return found

    return None


class DashboardService:

    def get_summary(self) -> dict:
        notes = []

        # Batch testing reports
        batch_reports = read_json_files("batch_*.json")

        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        recent_runs = []

        for path, report in batch_reports:
            metrics = find_metrics(report)

            if not metrics:
                continue

            total_tests += int(metrics.get("total_tests", 0))
            passed_tests += int(metrics.get("passed", 0))
            failed_tests += int(metrics.get("failed", 0))

            recent_runs.append({
                "module": "Batch Testing",
                "file": path.name,
                "total": metrics.get("total_tests", 0),
                "passed": metrics.get("passed", 0),
                "failed": metrics.get("failed", 0),
                "modified_at": path.stat().st_mtime_ns,
                "status": (
                    "PASS" if metrics.get("failed", 0) == 0 else "FAIL"
                )
            })

        if not batch_reports:
            notes.append("No batch test reports found.")

        # Reliability reports
        reliability_reports = read_json_files("reliability_*.json")
        latencies = []

        for path, report in reliability_reports:
            metrics = find_metrics(report)

            if not metrics:
                continue

            total_tests += int(metrics.get("total_tests", 0))
            passed_tests += int(metrics.get("passed", 0))
            failed_tests += int(metrics.get("failed", 0))

            latency = metrics.get("average_latency_ms")
            if latency is not None:
                latencies.append(float(latency))

            recent_runs.append({
                "module": "Reliability",
                "file": path.name,
                "total": metrics.get("total_tests", 0),
                "passed": metrics.get("passed", 0),
                "failed": metrics.get("failed", 0),
                "modified_at": path.stat().st_mtime_ns,
                "status": (
                    "PASS" if metrics.get("failed", 0) == 0 else "FAIL"
                )
            })

        # Security reports
        security_reports = read_json_files("security_*.json")
        security_scans = 0
        security_findings = 0

        for path, report in security_reports:
            metrics = find_metrics(report)

            if metrics:
                security_scans += int(metrics.get("total_tests", 0))
                security_findings += int(metrics.get("failed", 0))

        # Regression history files
        regression_files = read_json_files("*_history.json")
        regression_runs = 0
        regression_count = 0
        regression_history = []

        for path, history in regression_files:
            if not isinstance(history, list):
                continue

            for run in history:
                if not isinstance(run, dict):
                    continue

                regression_runs += 1
                count = int(run.get("regression_count", 0))
                regression_count += count

                regression_history.append({
                    "suite": run.get("suite_name", path.stem),
                    "pass_rate": run.get("pass_rate", 0),
                    "regression_count": count,
                    "status": run.get("status", "UNKNOWN")
                })

        if not security_reports:
            notes.append("No saved security reports found.")

        notes.append(
            "Quality evaluation history is not included because "
            "the current Day 4 evaluation endpoint does not persist reports."
        )

        total_tests += 0  # Security and regression are separate metrics.

        pass_rate = (
            passed_tests / total_tests * 100
            if total_tests else 0
        )
        recent_runs.sort(key=lambda run: run["modified_at"])
        latest_runs = recent_runs[-10:][::-1]
        for run in latest_runs:
            del run["modified_at"]

        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "pass_rate": round(pass_rate, 2),
            "security_scans": security_scans,
            "security_findings": security_findings,
            "reliability_runs": len(reliability_reports),
            "average_latency_ms": (
                round(mean(latencies), 2) if latencies else 0
            ),
            "regression_runs": regression_runs,
            "regression_count": regression_count,
            "recent_runs": latest_runs,
            "regression_history": regression_history[-10:][::-1],
            "data_notes": notes
        }