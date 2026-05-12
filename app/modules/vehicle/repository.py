"""Vehicle repository.

Encapsulates SQLAlchemy operations so service layer stays persistence-agnostic.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.vehicle.model import Vehicle


class VehicleRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_license_plate(self, license_plate: str) -> Vehicle | None:
        # Fast lookup by normalized unique license plate.
        stmt = select(Vehicle).where(Vehicle.license_plate == license_plate)
        return self.db.execute(stmt).scalar_one_or_none()

    def create(
        self,
        license_plate: str,
        driver_name: str,
        brand: str,
        model: str,
        color: str,
    ) -> Vehicle:
        # Create new vehicle aggregate root.
        vehicle = Vehicle(
            license_plate=license_plate,
            driver_name=driver_name,
            brand=brand,
            model=model,
            color=color,
        )
        self.db.add(vehicle)
        self.db.flush()
        return vehicle

    def update_metadata(
        self,
        vehicle: Vehicle,
        driver_name: str,
        brand: str,
        model: str,
        color: str,
    ) -> Vehicle:
        # Keep latest metadata when same vehicle re-enters with updated details.
        vehicle.driver_name = driver_name
        vehicle.brand = brand
        vehicle.model = model
        vehicle.color = color
        self.db.flush()
        return vehicle
