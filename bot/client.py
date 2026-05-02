"""Binance Futures Testnet REST API client."""

from __future__ import annotations

import hashlib
import hmac
import logging
import os
import time
from typing import Any
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv

from bot.exceptions import BinanceAPIError, ConfigurationError


DEFAULT_BASE_URL = "https://testnet.binancefuture.com"


class BinanceFuturesClient:
    """Small REST wrapper for signed Binance USDT-M Futures requests."""

    def __init__(
        self,
        api_key: str | None = None,
        api_secret: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = 10,
        logger: logging.Logger | None = None,
    ) -> None:
        load_dotenv()
        self.api_key = api_key or os.getenv("BINANCE_API_KEY")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.logger = logger or logging.getLogger("trading_bot")

        if not self.api_key or not self.api_secret:
            raise ConfigurationError(
                "Missing API credentials. Set BINANCE_API_KEY and "
                "BINANCE_API_SECRET in your environment or .env file."
            )

    def place_market_order(
        self,
        symbol: str,
        side: str,
        quantity: str,
    ) -> dict[str, Any]:
        """Place a MARKET order."""
        payload = {
            "symbol": symbol,
            "side": side,
            "type": "MARKET",
            "quantity": quantity,
            "newOrderRespType": "RESULT",
        }
        return self._signed_request("POST", "/fapi/v1/order", payload)

    def place_limit_order(
        self,
        symbol: str,
        side: str,
        quantity: str,
        price: str,
    ) -> dict[str, Any]:
        """Place a LIMIT order with good-til-canceled time in force."""
        payload = {
            "symbol": symbol,
            "side": side,
            "type": "LIMIT",
            "quantity": quantity,
            "price": price,
            "timeInForce": "GTC",
            "newOrderRespType": "RESULT",
        }
        return self._signed_request("POST", "/fapi/v1/order", payload)

    def _signed_request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any],
    ) -> dict[str, Any]:
        """Send a signed request to Binance and return JSON response."""
        request_params = {
            **params,
            "timestamp": int(time.time() * 1000),
            "recvWindow": 5000,
        }
        query_string = urlencode(request_params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        signed_query = f"{query_string}&signature={signature}"
        url = f"{self.base_url}{endpoint}"
        headers = {"X-MBX-APIKEY": self.api_key}

        self.logger.info(
            "API request | method=%s endpoint=%s params=%s",
            method,
            endpoint,
            self._redact_sensitive(request_params),
        )

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=signed_query,
                timeout=self.timeout,
            )
            response_data = response.json()
        except requests.RequestException as exc:
            self.logger.exception("Network failure while calling Binance API")
            raise BinanceAPIError(f"Network error: {exc}") from exc
        except ValueError as exc:
            self.logger.exception("Invalid JSON response from Binance API")
            raise BinanceAPIError("Invalid JSON response from Binance API.") from exc

        self.logger.info(
            "API response | status_code=%s response=%s",
            response.status_code,
            response_data,
        )

        if response.status_code >= 400:
            message = response_data.get("msg", "Binance API request failed.")
            code = response_data.get("code")
            raise BinanceAPIError(
                f"Binance API error {code}: {message}",
                status_code=response.status_code,
            )

        return response_data

    @staticmethod
    def _redact_sensitive(params: dict[str, Any]) -> dict[str, Any]:
        """Return request params safe for logging."""
        return {key: value for key, value in params.items() if key != "signature"}

