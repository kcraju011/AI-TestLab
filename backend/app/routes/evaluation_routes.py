from fastapi import APIRouter, HTTPException

from app.models.evaluation_schemas import (
    EvaluationRequest,
    EvaluationResponse
)

from app.evaluators.deepeval_evaluator import DeepEvalEvaluator


router = APIRouter(
    prefix="/api/v1/evaluations",
    tags=["AI Quality Evaluation"]
)


@router.post(
    "/run",
    response_model=EvaluationResponse
)
def run_evaluation(request: EvaluationRequest):

    try:
        evaluator = DeepEvalEvaluator()

        result = evaluator.evaluate(
            question=request.question,
            actual_answer=request.actual_answer,
            context=request.context,
            retrieval_context=request.retrieval_context
        )

        return {
            "question": request.question,
            "actual_answer": request.actual_answer,
            **result
        }

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"Evaluation failed: {str(error)}"
        )