import re

from app.shared.exceptions.base import ValidationError


LICENSE_PLATE_PATTERN = re.compile(r"^[A-Z0-9-]{3,20}$")


def normalize_license_plate(value: str) -> str:
    normalized = value.strip().upper()
    if not LICENSE_PLATE_PATTERN.match(normalized):
        raise ValidationError("Invalid license plate format.", code="INVALID_LICENSE_PLATE")
    return normalized
