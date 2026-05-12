from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db_session
from app.modules.parking.repository import ParkingSessionRepository
from app.modules.parking.schema import ParkingEntryRequest, ParkingExitRequest
from app.modules.parking.service import ParkingService
from app.modules.passkey.generator import NumericPasskeyGenerator
from app.modules.passkey.service import PasskeyService
from app.modules.passkey.validator import NumericPasskeyValidator
from app.modules.vehicle.repository import VehicleRepository
from app.shared.responses.base import success_response

router = APIRouter(prefix="/parking", tags=["parking"])


def get_parking_service(db: Session) -> ParkingService:
    passkey_service = PasskeyService(
        generator=NumericPasskeyGenerator(),
        validator=NumericPasskeyValidator(),
        max_retries=settings.passkey_max_retries,
    )
    return ParkingService(
        vehicle_repository=VehicleRepository(db),
        session_repository=ParkingSessionRepository(db),
        passkey_service=passkey_service,
        passkey_length=settings.passkey_length,
    )


@router.post("/entry", response_model=dict)
def create_entry(payload: ParkingEntryRequest, db: Session = Depends(get_db_session)) -> dict:
    service = get_parking_service(db)
    response = service.entry(payload)
    db.commit()
    return success_response(response.model_dump(), message="Vehicle entry logged.")


@router.post("/exit", response_model=dict)
def create_exit(payload: ParkingExitRequest, db: Session = Depends(get_db_session)) -> dict:
    service = get_parking_service(db)
    response = service.exit(payload)
    db.commit()
    return success_response(response.model_dump(), message="Vehicle exit logged.")


@router.get("/active", response_model=dict)
def list_active(db: Session = Depends(get_db_session)) -> dict:
    service = get_parking_service(db)
    response = service.get_active()
    return success_response([item.model_dump() for item in response], message="Active vehicles fetched.")


@router.get("/history", response_model=dict)
def list_history(db: Session = Depends(get_db_session)) -> dict:
    service = get_parking_service(db)
    response = service.get_history()
    return success_response([item.model_dump() for item in response], message="Parking history fetched.")
