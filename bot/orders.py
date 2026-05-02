"""Order placement business logic."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from bot.client import BinanceFuturesClient


@dataclass(frozen=True)
class OrderRequest:
    """Normalized order request accepted by the order service."""

    symbol: str
    side: str
    order_type: str
    quantity: str
    price: str | None = None


@dataclass(frozen=True)
class OrderResult:
    """Structured order response for CLI rendering."""

    order_id: int | str | None
    status: str | None
    executed_qty: str | None
    avg_price: str | None
    raw_response: dict[str, Any]


class OrderService:
    """Coordinates order business rules with the Binance client."""

    def __init__(
        self,
        client: BinanceFuturesClient,
        logger: logging.Logger | None = None,
    ) -> None:
        self.client = client
        self.logger = logger or logging.getLogger("trading_bot")

    def place_order(self, order_request: OrderRequest) -> OrderResult:
        """Place an order and return a normalized result."""
        self.logger.info("Placing order | request=%s", order_request)

        if order_request.order_type == "MARKET":
            response = self.client.place_market_order(
                symbol=order_request.symbol,
                side=order_request.side,
                quantity=order_request.quantity,
            )
        else:
            if order_request.price is None:
                raise ValueError("Limit order requires price.")
            response = self.client.place_limit_order(
                symbol=order_request.symbol,
                side=order_request.side,
                quantity=order_request.quantity,
                price=order_request.price,
            )

        result = OrderResult(
            order_id=response.get("orderId"),
            status=response.get("status"),
            executed_qty=response.get("executedQty"),
            avg_price=response.get("avgPrice"),
            raw_response=response,
        )
        self.logger.info("Order placed successfully | result=%s", result)
        return result

