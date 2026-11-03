import time
import uuid

from fastapi import APIRouter

from app.models.schemas import (
    TestRequest,
    TestResponse
)

from app.services.mock_llm import MockLLMService

from app.evaluators.basic_evaluator import BasicEvaluator


router = APIRouter(
    prefix="/api/v1/tests",
    tags=["AI Testing"]
)

llm_service = MockLLMService()

evaluator = BasicEvaluator()


@router.post("/run", response_model=TestResponse)
def run_test(request: TestRequest):

    start_time = time.perf_counter()

    actual_answer = llm_service.generate_response(
        question=request.question,
        expected_answer=request.expected_answer,
        scenario=request.scenario
    )

    evaluation = evaluator.evaluate(
        expected_answer=request.expected_answer,
        actual_answer=actual_answer
    )

    execution_time = (
        time.perf_counter() - start_time
    ) * 1000

    return TestResponse(
        test_id=str(uuid.uuid4()),
        question=request.question,
        expected_answer=request.expected_answer,
        actual_answer=actual_answer,
        score=evaluation["score"],
        status=evaluation["status"],
        execution_time_ms=round(execution_time, 2),
        message="AI test executed successfully"
    )