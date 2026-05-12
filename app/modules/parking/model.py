from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import ParkingSessionStatus
from app.core.database import Base
from app.shared.utils.datetime import utc_now


class ParkingSession(Base):
    __tablename__ = "parking_sessions"
    __table_args__ = (
        Index("ix_parking_sessions_vehicle_status", "vehicle_id", "status"),
        Index("ix_parking_sessions_status_entry_time", "status", "entry_time"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"), nullable=False, index=True)
    passkey: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    entry_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    exit_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[ParkingSessionStatus] = mapped_column(
        Enum(ParkingSessionStatus), default=ParkingSessionStatus.ACTIVE, nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False
    )

    vehicle = relationship("Vehicle", back_populates="sessions")
