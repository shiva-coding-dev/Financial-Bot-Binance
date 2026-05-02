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

if not api_key:
    print("No API Key")
    exit(1)

params = {"timestamp": int(time.time() * 1000), "recvWindow": 5000}
query = urlencode(params)
sig = hmac.new(api_secret.encode("utf-8"), query.encode("utf-8"), hashlib.sha256).hexdigest()
url = f"https://testnet.binancefuture.com/fapi/v2/account?{query}&signature={sig}"

resp = requests.get(url, headers={"X-MBX-APIKEY": api_key})
print(resp.status_code)
print(resp.text)
