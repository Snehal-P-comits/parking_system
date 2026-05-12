from app.modules.vehicle.model import Vehicle
from app.modules.vehicle.repository import VehicleRepository
from app.modules.vehicle.schema import VehicleCreateRequest
from app.shared.validators.license_plate import normalize_license_plate


class VehicleService:
    def __init__(self, repository: VehicleRepository) -> None:
        self.repository = repository

    def get_or_create(self, payload: VehicleCreateRequest) -> Vehicle:
        normalized_plate = normalize_license_plate(payload.license_plate)
        vehicle = self.repository.get_by_license_plate(normalized_plate)
        if vehicle is not None:
            return self.repository.update_metadata(
                vehicle=vehicle,
                driver_name=payload.driver_name,
                brand=payload.brand,
                model=payload.model,
                color=payload.color,
            )
        return self.repository.create(
            license_plate=normalized_plate,
            driver_name=payload.driver_name,
            brand=payload.brand,
            model=payload.model,
            color=payload.color,
        )
