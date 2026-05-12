"""Parking session repository."""

from sqlalchemy import Select, desc, select
from sqlalchemy.orm import Session, joinedload

from app.core.constants import ParkingSessionStatus
from app.modules.parking.model import ParkingSession


class ParkingSessionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_active_by_vehicle_id(self, vehicle_id: int) -> ParkingSession | None:
        # Enforces one-active-session lookup used by entry/exit services.
        stmt = select(ParkingSession).where(
            ParkingSession.vehicle_id == vehicle_id,
            ParkingSession.status == ParkingSessionStatus.ACTIVE,
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def create_session(self, vehicle_id: int, passkey: str) -> ParkingSession:
        # Create an ACTIVE session at entry time.
        session = ParkingSession(vehicle_id=vehicle_id, passkey=passkey, status=ParkingSessionStatus.ACTIVE)
        self.db.add(session)
        self.db.flush()
        self.db.refresh(session)
        return session

    def close_session(self, session: ParkingSession, exit_time) -> ParkingSession:
        # Mutate ACTIVE session to EXITED and persist exit timestamp.
        session.exit_time = exit_time
        session.status = ParkingSessionStatus.EXITED
        self.db.flush()
        self.db.refresh(session)
        return session

    def list_active(self) -> list[ParkingSession]:
        # Active board for currently parked vehicles.
        stmt = self._base_query().where(ParkingSession.status == ParkingSessionStatus.ACTIVE)
        return list(self.db.execute(stmt.order_by(desc(ParkingSession.entry_time))).scalars().all())

    def list_history(self) -> list[ParkingSession]:
        # Full audit trail (both ACTIVE and EXITED).
        stmt = self._base_query()
        return list(self.db.execute(stmt.order_by(desc(ParkingSession.entry_time))).scalars().all())

    def is_passkey_available_for_active_sessions(self, passkey: str) -> bool:
        # Uniqueness check intentionally scoped to ACTIVE sessions only.
        stmt = select(ParkingSession.id).where(
            ParkingSession.passkey == passkey,
            ParkingSession.status == ParkingSessionStatus.ACTIVE,
        )
        return self.db.execute(stmt).scalar_one_or_none() is None

    def _base_query(self) -> Select[tuple[ParkingSession]]:
        # Eager-load vehicle to avoid N+1 during history mapping.
        return select(ParkingSession).options(joinedload(ParkingSession.vehicle))
