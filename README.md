# Binance Futures Testnet Trading Bot

A CLI-based Python 3 trading bot for placing `MARKET` and `LIMIT` orders on Binance USDT-M Futures Testnet.

The project uses direct REST API calls to `https://testnet.binancefuture.com`, signs requests with HMAC SHA256, validates CLI input, logs requests/responses, and prints a concise order result.

## Project Structure

```text
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py
│   ├── orders.py
│   ├── validators.py
│   ├── logging_config.py
│   └── exceptions.py
├── cli.py
├── README.md
└── requirements.txt
```

## Setup

Create and activate a virtual environment:

```bash
cd trading_bot
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Add Binance Futures Testnet API credentials:

```bash
export BINANCE_API_KEY="your_testnet_api_key"
export BINANCE_API_SECRET="your_testnet_api_secret"
```

You can also create a `.env` file inside `trading_bot/`:

```env
BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_api_secret
```

## How To Run

Place a market order:

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

Place a limit order:

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 30000
```

## Sample Output

Market order:

```text
Order Request Summary
---------------------
Symbol      : BTCUSDT
Side        : BUY
Order Type  : MARKET
Quantity    : 0.01

Order Response
--------------
Order ID    : 123456789
Status      : FILLED
Executed Qty: 0.01
Avg Price   : 65000.10

Success: order submitted to Binance Futures Testnet.
```

Limit order:

```text
Order Request Summary
---------------------
Symbol      : BTCUSDT
Side        : SELL
Order Type  : LIMIT
Quantity    : 0.01
Price       : 30000

Order Response
--------------
Order ID    : 123456790
Status      : NEW
Executed Qty: 0
Avg Price   : 0.00000

Success: order submitted to Binance Futures Testnet.
```

Failure example:

```text
Failure: Price is required for LIMIT orders.
```

## Logging

Application logs are written to:

```text
logs/app.log
```

Logs include timestamps, log level, API request metadata, API responses, validation errors, configuration errors, and unexpected failures.

## Assumptions

- This bot is for Binance Futures Testnet only, not production trading.
- Credentials are provided through environment variables or a local `.env` file.
- `LIMIT` orders use `GTC` time in force.
- `MARKET` orders must not include a price.
- Quantity and price precision are left to Binance exchange filters. If the values are invalid for the selected symbol, Binance returns a clear API error.
- The CLI supports `MARKET` and `LIMIT` orders as required by the assignment.

