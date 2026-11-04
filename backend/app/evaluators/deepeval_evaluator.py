from typing import List

from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    HallucinationMetric
)

from deepeval.test_case import LLMTestCase

from app.core.config import settings


class DeepEvalEvaluator:

    def __init__(self):

        self.model = settings.DEEPEVAL_MODEL

    def evaluate(
        self,
        question: str,
        actual_answer: str,
        context: List[str],
        retrieval_context: List[str]
    ):

        answer_relevancy = AnswerRelevancyMetric(
            threshold=0.70,
            model=self.model,
            include_reason=True
        )

        faithfulness = FaithfulnessMetric(
            threshold=0.70,
            model=self.model,
            include_reason=True
        )

        hallucination = HallucinationMetric(
            threshold=0.70,
            model=self.model,
            include_reason=True
        )

        test_case = LLMTestCase(
            input=question,
            actual_output=actual_answer,
            context=context,
            retrieval_context=retrieval_context
        )

        # Metric 1: Answer relevance
        answer_relevancy.measure(test_case)

        # Metric 2: Faithfulness to retrieved information
        faithfulness.measure(test_case)

        # Metric 3: Consistency with trusted reference context
        hallucination.measure(test_case)

        def result(metric):
            return {
                "score": round(float(metric.score), 2),
                "threshold": metric.threshold,
                "passed": bool(metric.is_successful()),
                "reason": metric.reason
            }

        results = {
            "answer_relevancy": result(answer_relevancy),
            "faithfulness": result(faithfulness),
            "hallucination": result(hallucination)
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