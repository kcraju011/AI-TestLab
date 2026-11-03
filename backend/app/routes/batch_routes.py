from fastapi import APIRouter, HTTPException

from app.models.batch_schemas import (
    BatchRunRequest,
    BatchRunResponse
)

from app.services.batch_runner import BatchRunner


router = APIRouter(
    prefix="/api/v1/batches",
    tags=["Batch Testing"]
)


@router.post("/run", response_model=BatchRunResponse)
def run_batch(request: BatchRunRequest):

    try:
        runner = BatchRunner()

        result = runner.run_batch(
            provider=request.provider
        )

        return result

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"Batch execution failed: {str(error)}"
        )