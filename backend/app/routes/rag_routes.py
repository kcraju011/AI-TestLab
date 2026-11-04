from fastapi import APIRouter, HTTPException

from app.models.rag_schemas import (
    IngestResponse,
    RAGEvaluationRequest,
    RAGRequest,
    RAGResponse
)

from app.evaluators.rag_evaluator import RAGEvaluator
from app.services.rag_service import RAGService


router = APIRouter(
    prefix="/api/v1/rag",
    tags=["RAG Pipeline"]
)


@router.post(
    "/ingest",
    response_model=IngestResponse
)
def ingest_documents():

    try:
        service = RAGService()

        result = service.ingest_documents()

        return result

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Document ingestion failed: {str(error)}"
        )


@router.post(
    "/ask",
    response_model=RAGResponse
)
def ask_question(request: RAGRequest):

    try:
        service = RAGService()

        result = service.ask(
            question=request.question,
            top_k=request.top_k
        )

        return result

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"RAG execution failed: {str(error)}"
        )


@router.post("/evaluate")
def evaluate_rag(request: RAGEvaluationRequest):

    try:
        evaluator = RAGEvaluator()

        result = evaluator.evaluate(
            question=request.question,
            actual_answer=request.actual_answer,
            expected_answer=request.expected_answer,
            retrieval_context=request.retrieval_context
        )

        return {
            "question": request.question,
            **result
        }

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"RAG evaluation failed: {str(error)}"
        )