"""Parking use-case service.

Contains entry, exit, and query business workflows.
"""

from app.core.constants import ParkingSessionStatus
from app.modules.parking.repository import ParkingSessionRepository
from app.modules.parking.schema import (
    ParkingEntryRequest,
    ParkingEntryResponse,
    ParkingExitRequest,
    ParkingExitResponse,
    ParkingHistoryItem,
)
from app.modules.passkey.exceptions import InvalidPasskeyFormatError, PasskeyGenerationFailedError
from app.modules.passkey.service import PasskeyService
from app.modules.vehicle.repository import VehicleRepository
from app.modules.vehicle.service import VehicleService
from app.shared.exceptions.base import (
    AuthenticationError,
    ConflictError,
    NotFoundError,
    ValidationError,
)
from app.shared.utils.datetime import utc_now
from app.shared.validators.license_plate import normalize_license_plate


class ParkingService:
    def __init__(
        self,
        vehicle_repository: VehicleRepository,
        session_repository: ParkingSessionRepository,
        passkey_service: PasskeyService,
        passkey_length: int,
    ) -> None:
        # Compose dependencies once; keeps routes thin and logic centralized.
        self.vehicle_service = VehicleService(vehicle_repository)
        self.vehicle_repository = vehicle_repository
        self.session_repository = session_repository
        self.passkey_service = passkey_service
        self.passkey_length = passkey_length

    def entry(self, payload: ParkingEntryRequest) -> ParkingEntryResponse:
        # Vehicle identity is created/updated first, then session is opened.
        vehicle = self.vehicle_service.get_or_create(payload)
        active_session = self.session_repository.get_active_by_vehicle_id(vehicle.id)
        if active_session is not None:
            # Business guard: one active session per vehicle.
            raise ConflictError("Vehicle already has an active parking session.", code="ACTIVE_SESSION_EXISTS")

        try:
            # Generate passkey that is unique among active sessions.
            generated_passkey = self.passkey_service.generate_unique(
                length=self.passkey_length,
                uniqueness_checker=self.session_repository.is_passkey_available_for_active_sessions,
            )
        except PasskeyGenerationFailedError as exc:
            raise ConflictError(str(exc), code="PASSKEY_GENERATION_FAILED") from exc

        stored_passkey = self.passkey_service.transform(generated_passkey)
        # Store transformed key so hashing strategy can be introduced later.
        session = self.session_repository.create_session(vehicle_id=vehicle.id, passkey=stored_passkey)
        return ParkingEntryResponse(
            license_plate=vehicle.license_plate,
            passkey=generated_passkey,
            entry_time=session.entry_time,
            status=ParkingSessionStatus.ACTIVE,
        )

    def exit(self, payload: ParkingExitRequest) -> ParkingExitResponse:
        # Normalize first to match canonical license-plate storage format.
        normalized_plate = normalize_license_plate(payload.license_plate)
        vehicle = self.vehicle_repository.get_by_license_plate(normalized_plate)
        if vehicle is None:
            raise NotFoundError("Vehicle not found.", code="VEHICLE_NOT_FOUND")

        session = self.session_repository.get_active_by_vehicle_id(vehicle.id)
        if session is None:
            raise NotFoundError("No active session found for vehicle.", code="ACTIVE_SESSION_NOT_FOUND")

        try:
            # Validate user-supplied passkey shape before comparison.
            self.passkey_service.validate_or_raise(payload.passkey, self.passkey_length)
        except InvalidPasskeyFormatError as exc:
            raise ValidationError(str(exc), code="INVALID_PASSKEY_FORMAT") from exc

        candidate_passkey = self.passkey_service.transform(payload.passkey)
        # Compare transformed candidate to stored transformed key.
        if candidate_passkey != session.passkey:
            raise AuthenticationError("Invalid passkey.", code="INVALID_PASSKEY")

        closed_session = self.session_repository.close_session(session, exit_time=utc_now())
        return ParkingExitResponse(
            license_plate=vehicle.license_plate,
            passkey=payload.passkey,
            entry_time=closed_session.entry_time,
            exit_time=closed_session.exit_time,
            status=ParkingSessionStatus.EXITED,
        )

    def get_active(self) -> list[ParkingHistoryItem]:
        # Query-only use case for active dashboard.
        sessions = self.session_repository.list_active()
        return [self._map_history_item(session) for session in sessions]

    def get_history(self) -> list[ParkingHistoryItem]:
        # Query-only use case for historical reporting.
        sessions = self.session_repository.list_history()
        return [self._map_history_item(session) for session in sessions]

    @staticmethod
    def _map_history_item(session) -> ParkingHistoryItem:
        vehicle = session.vehicle
        return ParkingHistoryItem(
            session_id=session.id,
            license_plate=vehicle.license_plate,
            driver_name=vehicle.driver_name,
            brand=vehicle.brand,
            model=vehicle.model,
            color=vehicle.color,
            passkey=session.passkey,
            entry_time=session.entry_time,
            exit_time=session.exit_time,
            status=session.status,
        )
