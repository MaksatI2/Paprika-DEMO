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


BatchReserveCall = Callable[[list[tuple[str, int]]], set[str]]


def reserve_batch(lines: list[Line], reserve_many: BatchReserveCall) -> list[str]:
    """Reserve the whole cart in one inventory call; return the SKUs that could not be reserved."""
    failed = reserve_many([(line.sku, line.quantity) for line in lines])
    return [line.sku for line in lines if line.sku in failed]
