import time
from statistics import mean
import math


class ReliabilityEngine:

    def run_test(
        self,
        total_requests: int,
        simulated_delay_ms: int,
        failure_every: int = 0
    ) -> dict:

        latencies = []
        successful = 0
        failed = 0

        for request_number in range(1, total_requests + 1):

            start_time = time.perf_counter()

            try:
                time.sleep(simulated_delay_ms / 1000)

                if failure_every and request_number % failure_every == 0:
                    raise RuntimeError("Simulated service failure")

                successful += 1

            except RuntimeError:
                failed += 1

            latency = (time.perf_counter() - start_time) * 1000
            latencies.append(latency)

        success_rate = (successful / total_requests) * 100

        average_latency = mean(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)

        sorted_latencies = sorted(latencies)
        p95_index = max(
            0,
            math.ceil(0.95 * len(sorted_latencies)) - 1
        )
        p95_latency = sorted_latencies[p95_index]

        status = (
            "PASS"
            if failed == 0
            else "FAIL"
        )

        return {
            "total_requests": total_requests,
            "successful_requests": successful,
            "failed_requests": failed,
            "success_rate": round(success_rate, 2),
            "average_latency_ms": round(average_latency, 2),
            "min_latency_ms": round(min_latency, 2),
            "max_latency_ms": round(max_latency, 2),
            "p95_latency_ms": round(p95_latency, 2),
            "status": status
        }