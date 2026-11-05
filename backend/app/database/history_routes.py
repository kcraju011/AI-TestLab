from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.database_service import DatabaseService

router = APIRouter(
    prefix="/api/v1/history",
    tags=["Test History"],
)


@router.get("/")
def list_history(
    module: Optional[str] = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    runs = DatabaseService.get_history(
        db=db,
        module=module,
        limit=limit,
        offset=offset,
    )

    return {
        "count": len(runs),
        "items": runs,
    }


@router.get("/{run_id}")
def history_detail(
    run_id: int,
    db: Session = Depends(get_db),
):
    run = DatabaseService.get_run(db, run_id)

    if run is None:
        raise HTTPException(
            status_code=404,
            detail="Test run not found",
        )

    return run