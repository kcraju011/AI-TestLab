from typing import List

from deepeval.metrics import (
    ContextualRelevancyMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric
)

from deepeval.test_case import LLMTestCase

from app.core.config import settings


class RAGEvaluator:

    def __init__(self):

        self.model = settings.DEEPEVAL_MODEL

    def evaluate(
        self,
        question: str,
        actual_answer: str,
        expected_answer: str,
        retrieval_context: List[str]
    ):

        test_case = LLMTestCase(
            input=question,
            actual_output=actual_answer,
            expected_output=expected_answer,
            retrieval_context=retrieval_context
        )

        metrics = {
            "contextual_relevancy": ContextualRelevancyMetric(
                threshold=0.70,
                model=self.model,
                include_reason=True
            ),

            "contextual_precision": ContextualPrecisionMetric(
                threshold=0.70,
                model=self.model,
                include_reason=True
            ),

            "contextual_recall": ContextualRecallMetric(
                threshold=0.70,
                model=self.model,
                include_reason=True
            )
        }

        results = {}

        for name, metric in metrics.items():

            metric.measure(test_case)

            results[name] = {
                "score": round(float(metric.score), 2),
                "threshold": metric.threshold,
                "passed": bool(metric.is_successful()),
                "reason": metric.reason
            }

        overall_status = (
            "PASS"
            if all(item["passed"] for item in results.values())
            else "FAIL"
        )

        return {
            **results,
            "overall_status": overall_status
        }