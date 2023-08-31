import os
import json
import pickle
from arbitrage_trading.crypto_exchanges.binance import client, get_trading_pairs
from arbitrage_trading.crypto_exchanges.binance.wsbook import WsbookBinance


def arbitrage_watcher(ws, data):
    print("kkkkkkk")
    print(json.loads(data))
    print("lkk")


def on_close():
    print("### Closed ###")


def build_trading_pairs(*args) -> list:
    pairs = []
    stored_pairs_path = "".join(args)
    if os.path.exists(stored_pairs_path):
        with open(stored_pairs_path, "rb") as f:
            pairs = pickle.loads(f.read())
    else:
        for p in args:
            i = 0
            while args.__len__() > i:
                pair = p+args[i]
                if pair.upper() in get_trading_pairs():
                    pairs.append(pair.upper())
                i += 1
        with open(stored_pairs_path, "wb") as f:
            f.write(pickle.dumps(pairs))

    return pairs

def compute_triangular_arbitrage_opportinuty():
    pass

def triangular_arbitrage(*args):
    try:
        print(args.__len__(), args)
        t_pairs = build_trading_pairs(*list(args))
        print(t_pairs)
        t_pairs_data = {}
        # print(client.get_symbol_info('ETHBTC'))
        for pair in t_pairs:
            get_order = client.get_order_book(symbol=pair)
            trade_fee = client.get_trade_fee(symbol=pair)
            marker = trade_fee[0]['makerCommission']
            taker = trade_fee[0]['takerCommission']
            t_pairs_data[pair] = (get_order['bids'][0], get_order['asks'][0], marker, taker)

        print(t_pairs_data)
        # print(client.get_orderbook_tickers())
        if args.__len__() == 0:
            # find all triangular arbitrage opportunities
            binance = WsbookBinance("usdtbtc")
            binance.b_connect(arbitrage_watcher, on_close)
        else:
            # Only look for given assets arbitrage opportunity
            pass
    except Exception as e:
        print(e)
