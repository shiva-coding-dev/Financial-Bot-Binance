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

## Codebase Functionality Breakdown

The project follows a clean, modular structure. Below is an explanation of every core module:

### 1. `cli.py` (Entry Point)
This is the main user interface. It uses Python's `argparse` to capture command-line arguments (symbol, side, type, quantity, price), passes them to the validation layer, and orchestrates the order request through the `OrderService`. It also neatly formats the output response for the terminal.

### 2. `bot/client.py` (Binance API Client)
The `BinanceFuturesClient` is responsible for secure HTTP communication with Binance.
- **HMAC SHA256 Signing:** It handles the complex logic of signing requests using your `BINANCE_API_SECRET`, appending timestamps, and managing `recvWindow` for secure execution.
- **Routing:** Exposes simple methods like `place_market_order()` and `place_limit_order()`.
- **Error Handling:** It captures raw HTTP errors and unexpected JSON responses, wrapping them into a clean `BinanceAPIError`.

### 3. `bot/orders.py` (Business Logic)
This file houses the `OrderService` and data classes (`OrderRequest`, `OrderResult`).
- It acts as the "brain" between the CLI and the API Client. 
- It routes the structured `OrderRequest` to the correct endpoint (Market vs Limit) based on the order type, and returns a sanitized `OrderResult` that the CLI can easily print.

### 4. `bot/validators.py` (Data Sanitization)
This module ensures bad data never reaches Binance.
- Validates the trading symbol (e.g., must be 5-20 uppercase letters).
- Checks valid sides (`BUY`, `SELL`) and order types (`MARKET`, `LIMIT`).
- Uses Python's `Decimal` to strictly validate prices and quantities, ensuring they are positive numbers and properly formatted strings to avoid floating-point errors.

### 5. `bot/exceptions.py` (Custom Errors)
Contains custom exceptions like `ValidationError`, `ConfigurationError`, and `BinanceAPIError`. This ensures that when the bot fails, it gives you a human-readable reason rather than crashing with an ugly traceback stack.

### 6. `bot/logging_config.py` (Audit Logging)
Automatically provisions a `logs/` directory and records all background operations to `app.log`. This includes everything from input validation to raw Binance API responses, allowing developers to debug issues if an order is unexpectedly rejected.

## Web Application (Frontend & API)

The bot has been upgraded from a simple CLI tool into a fully functional web application featuring a stunning Glassmorphism UI.

### 1. `api.py` (FastAPI Backend)
A lightweight web server was added using **FastAPI** and **Uvicorn** to expose the bot's functionality to the web.
- Exposes a `POST /api/order` endpoint.
- Connects directly to the existing robust validation and API client routing logic.
- Serves as the bridge between the React frontend and the Binance API.

### 2. `frontend/` (React + Vite Web App)
A modern, blazing-fast frontend built with **React** and **Vite**.
- **Aesthetic**: Custom "Glassmorphism" styling (`index.css`) featuring a dark-mode theme, blurred frosted glass panels, glowing accents, and smooth CSS animations.
- **Components**: The unified dashboard (`App.jsx`) provides intuitive inputs for Symbol, Side, Order Type, Quantity, and Price.
- **Real-time Feedback**: Automatically displays loading spinners during requests and animated success or error states with detailed order summaries directly in the browser.

### Running the Web App

**1. Start the Backend:**
```bash
source .venv/bin/activate
uvicorn api:app --host 0.0.0.0 --port 8000
```

**2. Start the Frontend (in a new terminal):**
```bash
cd frontend
npm run dev
```

**3. Open the UI:**
Navigate to `http://localhost:5173` in your browser to start trading!
