from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.database_service import DatabaseService
from app.database.schemas import (
    TestRunCreate,
    TestRunResponse,
    TestCaseResponse
)


router = APIRouter(
    prefix="/api/v1/database",
    tags=["Database History"]
)


@router.post("/runs", response_model=TestRunResponse, status_code=201)
def save_test_run(
    payload: TestRunCreate,
    db: Session = Depends(get_db)
):
    try:
        return DatabaseService.create_run(db, payload)

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error)
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Could not save test run"
        ) from error


@router.get("/runs", response_model=List[TestRunResponse])
def list_test_runs(
    module: Optional[str] = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    return DatabaseService.get_history(
        db=db,
        module=module,
        limit=limit,
        offset=offset
    )


@router.get("/runs/{run_id}", response_model=TestRunResponse)
def get_test_run(
    run_id: int,
    db: Session = Depends(get_db)
):
    run = DatabaseService.get_run(db, run_id)

    if not run:
        raise HTTPException(
            status_code=404,
            detail="Test run not found"
        )

    return run


@router.get(
    "/runs/{run_id}/cases",
    response_model=List[TestCaseResponse]
)
def get_test_case_results(
    run_id: int,
    db: Session = Depends(get_db)
):
    run = DatabaseService.get_run(db, run_id)

    if not run:
        raise HTTPException(
            status_code=404,
            detail="Test run not found"
        )

    return run.results