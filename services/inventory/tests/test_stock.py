import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.stock import Stock  # noqa: E402


class StockTests(unittest.TestCase):
    def test_reserve_reduces_stock(self):
        stock = Stock({"SKU-1": 3})
        self.assertTrue(stock.reserve("SKU-1", 2))
        self.assertEqual(stock.available("SKU-1"), 1)

    def test_cannot_overbook(self):
        self.assertFalse(Stock({"SKU-1": 1}).reserve("SKU-1", 2))


if __name__ == "__main__":
    unittest.main()
