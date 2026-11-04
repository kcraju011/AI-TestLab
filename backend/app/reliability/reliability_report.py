import json
from pathlib import Path
from uuid import uuid4
from datetime import datetime, timezone

from app.reliability.reliability_engine import ReliabilityEngine


PROJECT_ROOT = Path(__file__).resolve().parents[3]
REPORTS_DIR = PROJECT_ROOT / "reports" / "reliability"


class ReliabilityReport:

    def __init__(self):
        self.engine = ReliabilityEngine()
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    def generate(
        self,
        total_requests: int,
        simulated_delay_ms: int,
        failure_every: int = 0
    ) -> dict:

        result = self.engine.run_test(
            total_requests=total_requests,
            simulated_delay_ms=simulated_delay_ms,
            failure_every=failure_every
        )

        report = {
            "report_id": str(uuid4()),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "test_type": "reliability",
            "results": result
        }

        filename = REPORTS_DIR / f"reliability_{report['report_id']}.json"

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(report, file, indent=4)

        report["report_file"] = str(filename)

        return report