import time
import os
import pprint
from dotenv import load_dotenv
from binance import Client

load_dotenv()

client = Client(os.environ.get("BINANCE_API_KEY"), os.environ.get("BINANE_API_SECRET"))


def get_trading_pairs() -> list:
    exchange_info = client.get_exchange_info()
    pairs = []
    for s in exchange_info['symbols']:
        pairs.append(s['symbol'])

    return pairs


# pprint.pprint(depth)

# get all symbol prices
prices = client.get_all_tickers()
# print(prices)

# get a deposit address for BTC
address = client.get_deposit_address(coin='BTC')

# print(address)
