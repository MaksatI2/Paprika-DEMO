"""Stock levels and reservations per SKU."""


class Stock:
    def __init__(self, levels: dict[str, int]):
        self._levels = dict(levels)

    def available(self, sku: str) -> int:
        return self._levels.get(sku, 0)

    def reserve(self, sku: str, quantity: int) -> bool:
        if quantity <= 0 or self.available(sku) < quantity:
            return False
        self._levels[sku] -= quantity
        return True
