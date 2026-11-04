from datetime import datetime, timezone
from typing import Dict, List, Optional

from sqlalchemy import (
    String,
    Integer,
    Float,
    DateTime,
    ForeignKey,
    JSON,
    Index
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class TestRun(Base):

    __tablename__ = "test_runs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    module: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )

    source_run_id: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )

    total_tests: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    passed: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    failed: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    pass_rate: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )

    average_latency_ms: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="UNKNOWN"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    results: Mapped[List["TestCaseResult"]] = relationship(
        back_populates="run",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_test_runs_module_created", "module", "created_at"),
    )


class TestCaseResult(Base):

    __tablename__ = "test_case_results"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    run_id: Mapped[int] = mapped_column(
        ForeignKey("test_runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    test_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    details: Mapped[Dict] = mapped_column(
        JSON,
        default=dict
    )

    run: Mapped["TestRun"] = relationship(
        back_populates="results"
    )