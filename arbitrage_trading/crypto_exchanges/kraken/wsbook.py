# Kraken Websocket API Order Book
#
# Usage: ./wsbook.py symbol depth

import sys
import json
from websocket import create_connection

from arbitrage_trading.crypto_exchanges import kraken


class WsbookKraken:
    def __init__(self, cmd, scope="public"):
        self.ws = None
        self.api_feed = "book"
        self.api_symbol = cmd[1].upper()
        self.api_depth = cmd[2]
        self.api_domain = "wss://ws.kraken.com/"
        if scope == "private":
            self.api_domain = "wss://ws-auth.kraken.com/"

        self.api_book = {"bid": {}, "ask": {}}
        self.api_data = '{"event":"subscribe", "subscription":{"name":"%(feed)s", "depth":%(depth)s, ' \
                        '"token":"%(token)s"}, "pair":["%(symbol)s"]}' % {"feed": self.api_feed,
                                                                          "depth": self.api_depth,
                                                                          "symbol": self.api_symbol,
                                                                          "token": kraken.get_websocket_token()}

        self.k_connect()
        self.send()

    def alarmfunction(self, signalnumber, frame):
        # signal.alarm(1)
        self.api_output_book()

    def dicttofloat(self, keyvalue):
        return float(keyvalue[0])

    def api_output_book(self):
        bid = sorted(self.api_book["bid"].items(), key=self.dicttofloat, reverse=True)
        ask = sorted(self.api_book["ask"].items(), key=self.dicttofloat)
        print("Bid\t\t\t\t\t\tAsk")
        for x in range(int(self.api_depth)):
            print("%(bidprice)s (%(bidvolume)s)\t\t\t\t%(askprice)s (%(askvolume)s)" % {"bidprice": bid[x][0],
                                                                                        "bidvolume": bid[x][1],
                                                                                        "askprice": ask[x][0],
                                                                                        "askvolume": ask[x][1]})

    def api_update_book(self, side, data):
        for x in data:
            price_level = x[0]
            if float(x[1]) != 0.0:
                self.api_book[side].update({price_level: float(x[1])})
            else:
                if price_level in self.api_book[side]:
                    self.api_book[side].pop(price_level)
        if side == "bid":
            self.api_book["bid"] = dict(
                sorted(self.api_book["bid"].items(), key=self.dicttofloat, reverse=True)[:int(self.api_depth)])
        elif side == "ask":
            self.api_book["ask"] = dict(
                sorted(self.api_book["ask"].items(), key=self.dicttofloat)[:int(self.api_depth)])

    # signal.signal(signal.SIGABRT, alarmfunction)

    def k_connect(self):
        try:
            self.ws = create_connection(self.api_domain)
        except Exception as error:
            print("WebSocket connection failed (%s)" % error)
            sys.exit(1)

    def send(self):
        try:
            self.ws.send(self.api_data)
        except Exception as error:
            print("Feed subscription failed (%s)" % error)
            self.ws.close()
            sys.exit(1)

    def get_data(self):
        try:
            self.api_data = self.ws.recv()
        except KeyboardInterrupt:
            self.ws.close()
            sys.exit(0)
        except Exception as error:
            print("WebSocket message failed (%s)" % error)
            self.ws.close()
            sys.exit(1)

        self.api_data = json.loads(self.api_data)
        if type(self.api_data) == list:
            if "as" in self.api_data[1]:
                self.api_update_book("ask", self.api_data[1]["as"])
                self.api_update_book("bid", self.api_data[1]["bs"])
                # signal.alarm(1)
            elif "a" in self.api_data[1] or "b" in self.api_data[1]:
                for x in self.api_data[1:len(self.api_data[1:]) - 1]:
                    if "a" in x:
                        self.api_update_book("ask", x["a"])
                    elif "b" in x:
                        self.api_update_book("bid", x["b"])
        try:
            #print(f"Bid: {list(self.api_book['bid'].keys())[0]}, Ask: {list(self.api_book['ask'].keys())[0]}")
            yield list(self.api_book['bid'].keys())[0], list(self.api_book['ask'].keys())[0]
        except IndexError:
            yield [], []
