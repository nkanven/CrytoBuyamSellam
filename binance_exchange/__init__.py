import time
import os
import pprint
from dotenv import load_dotenv
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager

load_dotenv()

client = Client(os.environ.get("BINANCE_API_KEY"), os.environ.get("BINANE_API_SECRET"))
# get market depth
depth = client.get_order_book(symbol='BTCUSDT')

pprint.pprint(depth)

# get all symbol prices
prices = client.get_all_tickers()
# print(prices)

# get a deposit address for BTC
address = client.get_deposit_address(coin='BTC')

print(address)
