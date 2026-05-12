from enum import Enum


class ParkingSessionStatus(str, Enum):
    ACTIVE = "ACTIVE"
    EXITED = "EXITED"


DEFAULT_PASSKEY_LENGTH = 4
DEFAULT_PASSKEY_MAX_RETRIES = 25
DEFAULT_API_PREFIX = "/api/v1"
