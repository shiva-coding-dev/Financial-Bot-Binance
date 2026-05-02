import os
import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("BINANCE_API_KEY", "")
api_secret = os.getenv("BINANCE_API_SECRET", "")

params = {"timestamp": int(time.time() * 1000), "recvWindow": 5000}
query = urlencode(params)
sig = hmac.new(api_secret.encode("utf-8"), query.encode("utf-8"), hashlib.sha256).hexdigest()

# test futures prod
url = f"https://fapi.binance.com/fapi/v2/account?{query}&signature={sig}"
resp = requests.get(url, headers={"X-MBX-APIKEY": api_key})
print("Prod Futures:", resp.status_code, resp.text)

# test spot prod
url2 = f"https://api.binance.com/api/v3/account?{query}&signature={sig}"
resp2 = requests.get(url2, headers={"X-MBX-APIKEY": api_key})
print("Prod Spot:", resp2.status_code, resp2.text)
