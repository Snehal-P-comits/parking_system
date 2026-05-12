"""Vehicle use-case service."""

from app.modules.vehicle.model import Vehicle
from app.modules.vehicle.repository import VehicleRepository
from app.modules.vehicle.schema import VehicleCreateRequest
from app.shared.validators.license_plate import normalize_license_plate


class VehicleService:
    def __init__(self, repository: VehicleRepository) -> None:
        self.repository = repository

    def get_or_create(self, payload: VehicleCreateRequest) -> Vehicle:
        # Normalize before lookup so plate identity stays canonical in storage.
        normalized_plate = normalize_license_plate(payload.license_plate)
        vehicle = self.repository.get_by_license_plate(normalized_plate)
        if vehicle is not None:
            # Existing vehicle: refresh metadata and reuse same identity.
            return self.repository.update_metadata(
                vehicle=vehicle,
                driver_name=payload.driver_name,
                brand=payload.brand,
                model=payload.model,
                color=payload.color,
            )
        # New vehicle: create record for downstream parking session creation.
        return self.repository.create(
            license_plate=normalized_plate,
            driver_name=payload.driver_name,
            brand=payload.brand,
            model=payload.model,
            color=payload.color,
        )
