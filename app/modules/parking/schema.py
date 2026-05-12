from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.constants import ParkingSessionStatus
from app.modules.vehicle.schema import VehicleCreateRequest


class ParkingEntryRequest(VehicleCreateRequest):
    pass


class ParkingEntryResponse(BaseModel):
    license_plate: str
    passkey: str
    entry_time: datetime
    status: ParkingSessionStatus

    model_config = ConfigDict(from_attributes=True)


class ParkingExitRequest(BaseModel):
    license_plate: str = Field(min_length=3, max_length=20)
    passkey: str = Field(min_length=4, max_length=8)


class ParkingExitResponse(BaseModel):
    license_plate: str
    passkey: str
    entry_time: datetime
    exit_time: datetime
    status: ParkingSessionStatus


class ParkingHistoryItem(BaseModel):
    session_id: int
    license_plate: str
    driver_name: str
    brand: str
    model: str
    color: str
    passkey: str
    entry_time: datetime
    exit_time: datetime | None
    status: ParkingSessionStatus
