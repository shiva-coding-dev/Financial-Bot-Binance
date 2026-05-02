"""Validation helpers for CLI order input."""

from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation

from bot.exceptions import ValidationError


VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}
SYMBOL_PATTERN = re.compile(r"^[A-Z0-9]{5,20}$")


def normalize_symbol(symbol: str) -> str:
    """Validate and normalize a futures symbol."""
    if not symbol:
        raise ValidationError("Symbol is required.")

    normalized = symbol.strip().upper()
    if not SYMBOL_PATTERN.fullmatch(normalized):
        raise ValidationError(
            "Symbol must be 5-20 uppercase letters/numbers, e.g. BTCUSDT."
        )
    return normalized


def normalize_side(side: str) -> str:
    """Validate and normalize order side."""
    normalized = side.strip().upper() if side else ""
    if normalized not in VALID_SIDES:
        raise ValidationError("Side must be BUY or SELL.")
    return normalized


def normalize_order_type(order_type: str) -> str:
    """Validate and normalize order type."""
    normalized = order_type.strip().upper() if order_type else ""
    if normalized not in VALID_ORDER_TYPES:
        raise ValidationError("Order type must be MARKET or LIMIT.")
    return normalized


def validate_positive_decimal(value: float | str, field_name: str) -> str:
    """Validate a positive decimal and return a Binance-friendly string."""
    try:
        decimal_value = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValidationError(f"{field_name} must be a valid number.") from exc

    if decimal_value <= 0:
        raise ValidationError(f"{field_name} must be greater than 0.")

    return format(decimal_value.normalize(), "f")


def validate_order_inputs(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float | str,
    price: float | str | None = None,
) -> dict[str, str | None]:
    """Validate all CLI inputs and return normalized values."""
    normalized_order_type = normalize_order_type(order_type)
    normalized_price = None

    if normalized_order_type == "LIMIT":
        if price is None:
            raise ValidationError("Price is required for LIMIT orders.")
        normalized_price = validate_positive_decimal(price, "Price")
    elif price is not None:
        raise ValidationError("Price should only be provided for LIMIT orders.")

    return {
        "symbol": normalize_symbol(symbol),
        "side": normalize_side(side),
        "order_type": normalized_order_type,
        "quantity": validate_positive_decimal(quantity, "Quantity"),
        "price": normalized_price,
    }

