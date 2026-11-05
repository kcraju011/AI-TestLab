from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.batch_persistence import save_batch_result
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
def run_batch(
    request: BatchRunRequest,
    db: Session = Depends(get_db)
):

    try:
        runner = BatchRunner()

        result = runner.run_batch(
            provider=request.provider
        )

        saved_run = save_batch_result(db, result)

        return {
            **result,
            "database_run_id": saved_run.id
        }

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