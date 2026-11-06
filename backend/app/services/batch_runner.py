import json
import time
import uuid

from app.services.mock_llm import MockLLMService
from app.services.openai_llm import OpenAILLMService
from app.evaluators.basic_evaluator import BasicEvaluator
from app.core.paths import BACKEND_DIR


DATASET_PATH = BACKEND_DIR / "app" / "datasets" / "sample_dataset.json"
REPORTS_DIR = BACKEND_DIR / "reports"


class BatchRunner:

    def __init__(self):
        self.evaluator = BasicEvaluator()

    def load_dataset(self):
        if not DATASET_PATH.exists():
            raise FileNotFoundError(
                f"Dataset not found: {DATASET_PATH}"
            )

        with open(DATASET_PATH, "r", encoding="utf-8") as file:
            dataset = json.load(file)

        if not isinstance(dataset, list):
            raise ValueError("Dataset must contain a JSON array.")

        return dataset

    def run_batch(self, provider: str = "mock"):

        dataset = self.load_dataset()

        if provider == "mock":
            llm = MockLLMService()

        elif provider == "openai":
            llm = OpenAILLMService()

        else:
            raise ValueError("Unsupported LLM provider.")

        batch_id = str(uuid.uuid4())

        results = []

        for test_case in dataset:

            start_time = time.perf_counter()

            if provider == "mock":
                response = llm.generate_response(
                    question=test_case["question"],
                    expected_answer=test_case["expected_answer"],
                    scenario=test_case["scenario"]
                )
            else:
                response = llm.generate_response(
                    question=test_case["question"]
                )

            actual_answer = response["text"]

            evaluation = self.evaluator.evaluate(
                expected_answer=test_case["expected_answer"],
                actual_answer=actual_answer
            )

            execution_time = (
                time.perf_counter() - start_time
            ) * 1000

            result = {
                "test_id": test_case["test_id"],
                "category": test_case["category"],
                "question": test_case["question"],
                "expected_answer": test_case["expected_answer"],
                "actual_answer": actual_answer,
                "score": evaluation["score"],
                "status": evaluation["status"],
                "execution_time_ms": round(execution_time, 2),
                "provider": response["provider"],
                "model": response.get("model")
            }

            results.append(result)

        total_tests = len(results)

        passed = sum(
            1 for result in results
            if result["status"] == "PASS"
        )

        failed = total_tests - passed

        average_score = (
            sum(result["score"] for result in results) / total_tests
            if total_tests > 0
            else 0.0
        )

        pass_rate = (
            (passed / total_tests) * 100
            if total_tests > 0
            else 0.0
        )

        summary = {
            "total_tests": total_tests,
            "passed": passed,
            "failed": failed,
            "average_score": round(average_score, 2),
            "pass_rate": round(pass_rate, 2)
        }

        report = {
            "batch_id": batch_id,
            "provider": provider,
            "summary": summary,
            "results": results
        }

        REPORTS_DIR.mkdir(parents=True, exist_ok=True)

        report_path = REPORTS_DIR / f"batch_{batch_id}.json"

        with open(report_path, "w", encoding="utf-8") as file:
            json.dump(report, file, indent=4)

        return {
            **report,
            "report_file": str(report_path)
        }