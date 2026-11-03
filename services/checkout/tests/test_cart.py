import sys
import unittest
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.cart import Line, subtotal, tax, total  # noqa: E402
from app.reservations import reserve_all, reserve_batch  # noqa: E402

LINES = [Line("SKU-1", 2, Decimal("19.99")), Line("SKU-2", 1, Decimal("5.00"))]


class CartTests(unittest.TestCase):
    def test_subtotal(self):
        self.assertEqual(subtotal(LINES), Decimal("44.98"))

    def test_tax_rounds_half_up(self):
        self.assertEqual(tax(Decimal("10.00")), Decimal("0.88"))

    def test_total_with_discount(self):
        self.assertEqual(total(LINES, Decimal("4.98")), Decimal("43.50"))

    def test_discount_never_goes_negative(self):
        self.assertEqual(total(LINES, Decimal("100")), Decimal("0.00"))


class ReservationTests(unittest.TestCase):
    def test_reports_failed_skus(self):
        stock = {"SKU-1": 5, "SKU-2": 0}
        self.assertEqual(reserve_all(LINES, lambda sku, qty: stock[sku] >= qty), ["SKU-2"])

    def test_batch_makes_one_call(self):
        calls = []

        def reserve_many(items):
            calls.append(items)
            return {"SKU-2"}

        self.assertEqual(reserve_batch(LINES, reserve_many), ["SKU-2"])
        self.assertEqual(len(calls), 1)


if __name__ == "__main__":
    unittest.main()
