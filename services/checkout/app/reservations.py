"""Reserve stock in inventory before a payment is taken."""

from collections.abc import Callable

from app.cart import Line

ReserveCall = Callable[[str, int], bool]


def reserve_all(lines: list[Line], reserve: ReserveCall) -> list[str]:
    """Reserve every line; return the SKUs that could not be reserved."""
    failed = []
    for line in lines:
        if not reserve(line.sku, line.quantity):
            failed.append(line.sku)
    return failed
