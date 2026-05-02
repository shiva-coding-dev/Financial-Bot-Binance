"""CLI entry point for the Binance Futures Testnet trading bot."""

from __future__ import annotations

import argparse
import sys

from bot.client import BinanceFuturesClient
from bot.exceptions import BinanceAPIError, ConfigurationError, ValidationError
from bot.logging_config import setup_logging
from bot.orders import OrderRequest, OrderResult, OrderService
from bot.validators import validate_order_inputs


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Place MARKET and LIMIT orders on Binance Futures Testnet."
    )
    parser.add_argument("--symbol", required=True, help="Trading symbol, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument(
        "--type",
        dest="order_type",
        required=True,
        help="Order type: MARKET or LIMIT",
    )
    parser.add_argument("--quantity", required=True, help="Order quantity, e.g. 0.01")
    parser.add_argument("--price", required=False, help="Limit order price")
    return parser


def print_order_summary(order_request: OrderRequest) -> None:
    """Print a formatted order request summary."""
    print("\nOrder Request Summary")
    print("---------------------")
    print(f"Symbol      : {order_request.symbol}")
    print(f"Side        : {order_request.side}")
    print(f"Order Type  : {order_request.order_type}")
    print(f"Quantity    : {order_request.quantity}")
    if order_request.price:
        print(f"Price       : {order_request.price}")


def print_order_response(result: OrderResult) -> None:
    """Print the normalized order response."""
    print("\nOrder Response")
    print("--------------")
    print(f"Order ID    : {result.order_id}")
    print(f"Status      : {result.status}")
    print(f"Executed Qty: {result.executed_qty}")
    print(f"Avg Price   : {result.avg_price or 'N/A'}")
    print("\nSuccess: order submitted to Binance Futures Testnet.")


def main() -> int:
    """Parse CLI args, validate input, place order, and print output."""
    parser = build_parser()
    args = parser.parse_args()
    logger = setup_logging()

    try:
        validated = validate_order_inputs(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )
        order_request = OrderRequest(
            symbol=str(validated["symbol"]),
            side=str(validated["side"]),
            order_type=str(validated["order_type"]),
            quantity=str(validated["quantity"]),
            price=validated["price"],
        )
        client = BinanceFuturesClient(logger=logger)
        service = OrderService(client=client, logger=logger)
        print_order_summary(order_request)
        result = service.place_order(order_request)
        print_order_response(result)
        return 0

    except ValidationError as exc:
        logger.error("Validation error: %s", exc)
        print(f"\nFailure: {exc}", file=sys.stderr)
    except ConfigurationError as exc:
        logger.error("Configuration error: %s", exc)
        print(f"\nFailure: {exc}", file=sys.stderr)
    except BinanceAPIError as exc:
        logger.error("Binance API error: %s", exc)
        print(f"\nFailure: {exc}", file=sys.stderr)
    except Exception as exc:  # Defensive top-level guard for CLI stability.
        logger.exception("Unexpected error")
        print(f"\nFailure: unexpected error: {exc}", file=sys.stderr)

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
