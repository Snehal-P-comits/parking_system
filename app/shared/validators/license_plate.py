"""Configurable, country-aware vehicle license plate validation.

This module is intentionally framework-independent so it can be reused across
parking systems, OCR pipelines, and registry integrations.
"""

from dataclasses import asdict, dataclass
import re

from app.shared.exceptions.base import ValidationError


@dataclass(slots=True)
class PlateComponents:
    state_code: str
    rto_code: str
    series: str
    number: str


@dataclass(slots=True)
class PlateValidationResult:
    # Structured output for machine + human friendly validation feedback.
    valid: bool
    reason: str | None = None
    normalized: str | None = None
    components: dict[str, str] | None = None
    code: str | None = None


@dataclass(slots=True)
class CountryPlateSpec:
    # Country-specific regex and optional future hooks.
    pattern: re.Pattern[str]


COUNTRY_PLATE_SPECS: dict[str, CountryPlateSpec] = {
    "IN": CountryPlateSpec(
        pattern=re.compile(r"^([A-Z]{2})(\d{2})([A-Z]{1,2})(\d{4})$"),
    )
}


def normalize_plate(value: str) -> str:
    # Canonical normalization used before any structural validation.
    return value.strip().upper()


def format_plate(value: str, style: str = "compact", country: str = "IN") -> str:
    # Best-effort formatting helper for UI or downstream display.
    result = validate_components(value=value, country=country)
    if not result.valid or result.components is None:
        return normalize_plate(value)
    if style == "compact":
        return result.normalized or normalize_plate(value)
    if style == "spaced":
        component = result.components
        return f"{component['state_code']} {component['rto_code']} {component['series']} {component['number']}"
    return result.normalized or normalize_plate(value)


def validate_structure(value: str, country: str = "IN") -> PlateValidationResult:
    # Step 1: reject whitespace and unsupported country configs early.
    normalized = normalize_plate(value)
    if " " in value:
        return PlateValidationResult(
            valid=False,
            reason="License plate must not contain spaces.",
            normalized=normalized,
            code="PLATE_SPACES_NOT_ALLOWED",
        )
    if any(ch.isspace() for ch in value):
        return PlateValidationResult(
            valid=False,
            reason="License plate must not contain whitespace characters.",
            normalized=normalized,
            code="PLATE_WHITESPACE_NOT_ALLOWED",
        )

    spec = COUNTRY_PLATE_SPECS.get(country)
    if spec is None:
        return PlateValidationResult(
            valid=False,
            reason=f"Unsupported country code: {country}.",
            normalized=normalized,
            code="UNSUPPORTED_COUNTRY_CODE",
        )

    match = spec.pattern.fullmatch(normalized)
    if match is None:
        return PlateValidationResult(
            valid=False,
            reason="Invalid registration number structure.",
            normalized=normalized,
            code="INVALID_PLATE_STRUCTURE",
        )
    return PlateValidationResult(valid=True, normalized=normalized)


def validate_components(value: str, country: str = "IN") -> PlateValidationResult:
    # Step 2: parse regex groups and verify each semantic section.
    structure = validate_structure(value=value, country=country)
    if not structure.valid:
        return structure

    spec = COUNTRY_PLATE_SPECS[country]
    match = spec.pattern.fullmatch(structure.normalized or "")
    if match is None:
        return PlateValidationResult(
            valid=False,
            reason="Invalid registration number structure.",
            normalized=structure.normalized,
            code="INVALID_PLATE_STRUCTURE",
        )

    state_code, rto_code, series, number = match.groups()
    components = PlateComponents(
        state_code=state_code,
        rto_code=rto_code,
        series=series,
        number=number,
    )

    state_check = validate_state_code(state_code=components.state_code, country=country)
    if not state_check.valid:
        return PlateValidationResult(
            valid=False,
            reason=state_check.reason,
            normalized=structure.normalized,
            components=asdict(components),
            code=state_check.code,
        )

    if not components.rto_code.isdigit() or len(components.rto_code) != 2:
        return PlateValidationResult(
            valid=False,
            reason="Invalid RTO code format.",
            normalized=structure.normalized,
            components=asdict(components),
            code="INVALID_RTO_CODE_FORMAT",
        )
    if not components.series.isalpha() or len(components.series) not in (1, 2):
        return PlateValidationResult(
            valid=False,
            reason="Invalid series format.",
            normalized=structure.normalized,
            components=asdict(components),
            code="INVALID_SERIES_FORMAT",
        )
    if not components.number.isdigit() or len(components.number) != 4:
        return PlateValidationResult(
            valid=False,
            reason="Invalid number format.",
            normalized=structure.normalized,
            components=asdict(components),
            code="INVALID_NUMBER_FORMAT",
        )
    return PlateValidationResult(
        valid=True,
        normalized=structure.normalized,
        components=asdict(components),
    )


def validate_state_code(state_code: str, country: str = "IN") -> PlateValidationResult:
    # Current policy is structural-only state validation for India.
    if country != "IN":
        return PlateValidationResult(
            valid=False,
            reason=f"Unsupported country code: {country}.",
            code="UNSUPPORTED_COUNTRY_CODE",
        )
    if len(state_code) != 2 or not state_code.isalpha() or not state_code.isupper():
        return PlateValidationResult(
            valid=False,
            reason="Invalid state code format.",
            code="INVALID_STATE_CODE_FORMAT",
        )
    return PlateValidationResult(valid=True)


def normalize_license_plate(value: str, country: str = "IN") -> str:
    # Backward-compatible adapter for existing service-layer call sites.
    result = validate_components(value=value, country=country)
    if not result.valid:
        raise ValidationError(result.reason or "Invalid license plate format.", code=result.code or "INVALID_LICENSE_PLATE")
    return result.normalized or normalize_plate(value)
