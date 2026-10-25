import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.charges import ProviderTimeout, charge  # noqa: E402


class ChargeTests(unittest.TestCase):
    def test_returns_charge_id(self):
        self.assertEqual(charge(1999, "tok", lambda amount, token: "ch_1"), "ch_1")

    def test_rejects_non_positive_amounts(self):
        with self.assertRaises(ValueError):
            charge(0, "tok", lambda amount, token: "ch_1")

    @mock.patch("app.charges.time.sleep")
    def test_retries_timeouts(self, _sleep):
        calls = iter([ProviderTimeout(), "ch_2"])

        def call(amount, token):
            result = next(calls)
            if isinstance(result, Exception):
                raise result
            return result

        self.assertEqual(charge(500, "tok", call), "ch_2")


if __name__ == "__main__":
    unittest.main()
