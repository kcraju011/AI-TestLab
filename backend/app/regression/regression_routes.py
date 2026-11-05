from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.database_service import DatabaseService
from app.regression.schemas import (
    RegressionRequest,
    RegressionResponse,
)
from app.regression.regression_service import compare_and_save


router = APIRouter(
    prefix="/api/v1/regression",
    tags=["Regression Testing"],
)


@router.post(
    "/compare",
    response_model=RegressionResponse,
)
def compare_models(
    request: RegressionRequest,
    db: Session = Depends(get_db),
):
    try:
        return compare_and_save(db, request)

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to save regression comparison",
        )


@router.get("/history")
def regression_history(
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    if limit < 1 or limit > 100 or offset < 0:
        raise HTTPException(
            status_code=422,
            detail="Invalid pagination values",
        )

    runs = DatabaseService.get_history(
        db=db,
        module="regression",
        limit=limit,
        offset=offset,
    )

    return {
        "count": len(runs),
        "items": runs,
    }