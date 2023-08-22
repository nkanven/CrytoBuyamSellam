import json
from arbitrage_trading.crypto_exchanges.kraken.wsbook import WsbookKraken
from arbitrage_trading.crypto_exchanges.binance.wsbook import WsbookBinance
from arbitrage_trading.utils import notify
from models import Database

class CryptoExchanges(WsbookBinance, WsbookKraken):
    def __init__(self, args):
        WsbookKraken.__init__(self, args)
        WsbookBinance.__init__(self)
        self.database = Database()

    def arbitrage_watcher(self, ws, data):
        try:
            prices = json.loads(data)
            b_prices = (prices['b'], prices['a'])
            k_prices = list(self.get_data())[0]
            ratios = (float(b_prices[1]) - float(k_prices[0])) * 100 / float(k_prices[0])
            print("Binance ", b_prices)
            print("Kraken ", k_prices)
            t_text = "Price ratio {:.2f}% Buy {:.5f} on Kraken and sell {:.5f} on Binance".format(
                ratios, float(k_prices[0]), float(b_prices[1])
            )
            print(t_text)

            if ratios >= 1.5:
                text = ("Arbitrage opportunity between Kraken and Binance. "
                        "Buy {:.5f} on Kraken, Sell at {:.5f} on Binance for a {:.2f}% potential profit".format(
                            float(k_prices[0]), float(b_prices[1]), ratios
                            )

                        )
                notify(text)

        except Exception as e:
            print(str(e))

    def on_close(self):
        print("### Closed ###")

    def start(self):
        # self.b_connect(self.arbitrage_watcher, self.on_close)
        self.database.get_all_distinct_assets()

