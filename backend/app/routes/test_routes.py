import time
import uuid

from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    TestRequest,
    TestResponse
)

from app.services.mock_llm import MockLLMService

from app.services.openai_llm import (
    OpenAILLMService,
    LLMProviderError
)

from app.evaluators.basic_evaluator import BasicEvaluator


router = APIRouter(
    prefix="/api/v1/tests",
    tags=["AI Testing"]
)

mock_service = MockLLMService()

evaluator = BasicEvaluator()


@router.post("/run", response_model=TestResponse)
def run_test(request: TestRequest):

    start_time = time.perf_counter()

    try:

        if request.provider == "mock":

            result = mock_service.generate_response(
                question=request.question,
                expected_answer=request.expected_answer,
                scenario=request.scenario
            )

        elif request.provider == "openai":

            openai_service = OpenAILLMService()

            result = openai_service.generate_response(
                question=request.question
            )

        else:

            raise HTTPException(
                status_code=400,
                detail="Unsupported LLM provider"
            )

        actual_answer = result["text"]

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
            provider=result["provider"],
            model=result["model"],
            input_tokens=result["input_tokens"],
            output_tokens=result["output_tokens"],
            message="AI test executed successfully"
        )

    except LLMProviderError as error:

        raise HTTPException(
            status_code=502,
            detail=str(error)
        ) from error