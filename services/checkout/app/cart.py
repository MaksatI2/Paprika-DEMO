"""Cart totals for checkout: subtotal, discount and sales tax."""

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

TAX_RATE = Decimal("0.0875")
CENT = Decimal("0.01")


@dataclass(frozen=True)
class Line:
    sku: str
    quantity: int
    unit_price: Decimal


def subtotal(lines: list[Line]) -> Decimal:
    return sum((line.unit_price * line.quantity for line in lines), Decimal("0"))


def tax(amount: Decimal) -> Decimal:
    return (amount * TAX_RATE).quantize(CENT, ROUND_HALF_UP)


def total(lines: list[Line], discount: Decimal = Decimal("0")) -> Decimal:
    """Tax each line on its own (needed for per-item tax rules), then take the discount and its tax off."""
    taxed = sum((amount + tax(amount) for amount in (line.unit_price * line.quantity for line in lines)), Decimal("0"))
    return max(taxed - discount - tax(discount), Decimal("0"))
