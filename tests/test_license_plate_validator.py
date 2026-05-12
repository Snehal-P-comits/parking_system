"""Unit tests for reusable Indian license plate validator."""

import unittest

from app.shared.validators.license_plate import (
    format_plate,
    normalize_license_plate,
    normalize_plate,
    validate_components,
    validate_structure,
)


class TestIndianLicensePlateValidator(unittest.TestCase):
    # Happy-path samples taken from expected Indian plate structure.
    def test_valid_plates(self) -> None:
        for plate in ("TN07CM2026", "KA01AB1234", "MH12DE1433"):
            result = validate_components(plate)
            self.assertTrue(result.valid)
            self.assertIsNotNone(result.components)
            self.assertEqual(result.normalized, plate)

    def test_lowercase_normalization(self) -> None:
        result = validate_components("tn07cm2026")
        self.assertTrue(result.valid)
        self.assertEqual(result.normalized, "TN07CM2026")
        self.assertEqual(normalize_license_plate("tn07cm2026"), "TN07CM2026")

    def test_reject_space(self) -> None:
        # Whitespace is rejected with explicit reason code.
        result = validate_structure("TN 07CM2026")
        self.assertFalse(result.valid)
        self.assertEqual(result.code, "PLATE_SPACES_NOT_ALLOWED")

    def test_reject_special_character(self) -> None:
        result = validate_components("TN07-CM2026")
        self.assertFalse(result.valid)
        self.assertEqual(result.code, "INVALID_PLATE_STRUCTURE")

    def test_reject_bad_rto_length(self) -> None:
        result = validate_components("TN7CM2026")
        self.assertFalse(result.valid)
        self.assertEqual(result.code, "INVALID_PLATE_STRUCTURE")

    def test_reject_bad_number_length(self) -> None:
        result = validate_components("TN07CM202")
        self.assertFalse(result.valid)
        self.assertEqual(result.code, "INVALID_PLATE_STRUCTURE")

    def test_unknown_country(self) -> None:
        result = validate_structure("TN07CM2026", country="US")
        self.assertFalse(result.valid)
        self.assertEqual(result.code, "UNSUPPORTED_COUNTRY_CODE")

    def test_format_spaced(self) -> None:
        formatted = format_plate("mh12de1433", style="spaced")
        self.assertEqual(formatted, "MH 12 DE 1433")

    def test_normalize_plate_helper(self) -> None:
        self.assertEqual(normalize_plate(" ka01ab1234 "), "KA01AB1234")


if __name__ == "__main__":
    unittest.main()
