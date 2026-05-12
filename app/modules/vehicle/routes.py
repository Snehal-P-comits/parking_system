from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.modules.vehicle.repository import VehicleRepository
from app.modules.vehicle.schema import VehicleCreateRequest, VehicleResponse
from app.modules.vehicle.service import VehicleService
from app.shared.responses.base import success_response

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.post("", response_model=dict)
def upsert_vehicle(payload: VehicleCreateRequest, db: Session = Depends(get_db_session)) -> dict:
    service = VehicleService(repository=VehicleRepository(db))
    vehicle = service.get_or_create(payload)
    db.commit()
    return success_response(VehicleResponse.model_validate(vehicle).model_dump(), message="Vehicle upserted.")
