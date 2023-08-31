import os
import json
import pickle
from arbitrage_trading.crypto_exchanges.binance import client, get_trading_pairs
from arbitrage_trading.crypto_exchanges.binance.wsbook import WsbookBinance
from binance.enums import *


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
                pair = p + args[i]
                if pair.upper() in get_trading_pairs():
                    pairs.append(pair.upper())
                i += 1
        with open(stored_pairs_path, "wb") as f:
            f.write(pickle.dumps(pairs))

    return pairs


def arbitrage_paths(pairs_trio, pairs_info, path=1):
    print(pairs_trio)
    if path == 1:
        cross_rate = (1 / float(pairs_info[pairs_trio[0]][1][0])) * float(pairs_info[pairs_trio[1]][0][0]) * float(pairs_info[pairs_trio[2]][0][0])
        _rate = 1 + float(pairs_info[pairs_trio[0]][3]) + float(pairs_info[pairs_trio[1]][2]) + float(pairs_info[pairs_trio[2]][2])
    else:
        cross_rate = (1 / float(pairs_info[pairs_trio[0]][1][0])) * (1 / float(pairs_info[pairs_trio[1]][1][0])) * float(pairs_info[pairs_trio[2]][0][0])
        _rate = 1 + float(pairs_info[pairs_trio[0]][3]) + float(pairs_info[pairs_trio[1]][3]) + float(
            pairs_info[pairs_trio[2]][2])

    profit = 1 - (float(pairs_info[pairs_trio[1]][0][0]) * float(pairs_info[pairs_trio[2]][0][0]))

    return str(cross_rate), _rate, profit


def compute_triangular_arbitrage_opportinuty(pairs_info):
    cross_rate: float
    trade_order = [0, 0, 0]
    for key, value in pairs_info.items():
        cross_rate = (1 / float(pairs_info[key][1][0]))
        if trade_order[0] == 0:
            trade_order[0] = key
            continue
        if key.startswith(trade_order[0][:2]):
            trade_order[1] = key
        else:
            trade_order[2] = key

    print(arbitrage_paths(trade_order, pairs_info))

    trade_order.reverse()

    print(arbitrage_paths(trade_order, pairs_info))


    # order = client.create_test_order(
    #     symbol="ETHUSDT",
    #     side=SIDE_BUY,
    #     type=ORDER_TYPE_MARKET,
    #     quantity=1
    # )
    # print(order)
    # order = client.create_test_order(
    #     symbol="ETHUSDT",
    #     side=SIDE_SELL,
    #     type=ORDER_TYPE_MARKET,
    #     quantity=1
    # )
    # print(order)
    # order = client.create_test_order(
    #     symbol="BTCUSDT",
    #     side=SIDE_SELL,
    #     type=ORDER_TYPE_MARKET,
    #     quantity=1
    # )
    # print(order)

    # if cross_rate > _rate:
    #     print("Arbitrage opportunity")
    # else:
    #     print(f"Low cross rate {cross_rate}, rate {_rate}")


def trade_ordering(arbitrage_pairs):
    trade_order = {}
    for pair in arbitrage_pairs:
        for p in arbitrage_pairs:
            if p == pair:
                trade_order[p] = "buy"
            else:
                trade_order[pair] = "sell"

    return trade_order


def triangular_arbitrage(*args):
    """
    Spotting arbitrage trading opportunity
    :param args: symbols to combine for arbitrage
    :return: void
    """
    try:
        t_pairs = build_trading_pairs(*list(args))
        # print(t_pairs)
        t_pairs_data = {}
        # print(client.get_symbol_info('ETHBTC'))
        for pair in t_pairs:
            get_order = client.get_order_book(symbol=pair)
            trade_fee = client.get_trade_fee(symbol=pair)
            marker = trade_fee[0]['makerCommission']
            taker = trade_fee[0]['takerCommission']
            t_pairs_data[pair] = (get_order['bids'][0], get_order['asks'][0], marker, taker)

        # print(t_pairs_data)
        compute_triangular_arbitrage_opportinuty(t_pairs_data)
        # print(trade_ordering(t_pairs))
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
