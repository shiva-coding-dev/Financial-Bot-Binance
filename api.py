from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from bot.client import BinanceFuturesClient
from bot.orders import OrderRequest, OrderService
from bot.validators import validate_order_inputs
from bot.logging_config import setup_logging
from bot.exceptions import BinanceAPIError, ConfigurationError, ValidationError

app = FastAPI(title="Binance Futures Trading Bot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to the specific frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = setup_logging()

class OrderInput(BaseModel):
    symbol: str
    side: str
    order_type: str
    quantity: str
    price: Optional[str] = None

@app.post("/api/order")
def place_order(order_input: OrderInput):
    try:
        validated = validate_order_inputs(
            symbol=order_input.symbol,
            side=order_input.side,
            order_type=order_input.order_type,
            quantity=order_input.quantity,
            price=order_input.price,
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
        result = service.place_order(order_request)
        return {
            "success": True,
            "data": {
                "order_id": result.order_id,
                "status": result.status,
                "executed_qty": result.executed_qty,
                "avg_price": result.avg_price,
            }
        }
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except ConfigurationError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except BinanceAPIError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        logger.exception("Unexpected API error")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
