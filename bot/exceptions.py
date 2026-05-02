"""Custom exceptions used by the trading bot."""


class TradingBotError(Exception):
    """Base exception for all trading bot errors."""


class ValidationError(TradingBotError):
    """Raised when user input fails validation."""


class ConfigurationError(TradingBotError):
    """Raised when required configuration is missing or invalid."""


class BinanceAPIError(TradingBotError):
    """Raised when Binance returns an API-level error."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        self.status_code = status_code
        super().__init__(message)

