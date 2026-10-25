"""Charge a card through the payment provider, retrying transient failures."""

import time
from collections.abc import Callable


class ProviderTimeout(Exception):
    """The provider did not answer in time."""


def charge(amount_cents: int, token: str, call: Callable[[int, str], str], attempts: int = 3) -> str:
    """Return the provider's charge id; retry timeouts up to ``attempts`` times."""
    if amount_cents <= 0:
        raise ValueError("amount must be positive")
    for attempt in range(1, attempts + 1):
        try:
            return call(amount_cents, token)
        except ProviderTimeout:
            if attempt == attempts:
                raise
            time.sleep(0.2)
    raise RuntimeError("unreachable")
