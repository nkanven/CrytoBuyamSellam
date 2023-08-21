import sys
from arbitrage_trading.crypto_exchanges import CryptoExchanges
from arbitrage_trading.crypto_exchanges.kraken import *
from arbitrage_trading.crypto_exchanges.kucoin import *

print(client.get_account_summary_info())
# exit(11)

# get_account_balance()
# get_deposit_method("ETH")
# get_address("ETH", assets_method_mapping["ETH"])
# exit()

print(sys.argv)
if len(sys.argv) < 3:
    print("Usage: %s symbol depth" % sys.argv[0])
    print("Example: %s xbt/usd 10" % sys.argv[0])
    sys.exit(1)

crypto_exchage = CryptoExchanges(sys.argv)
crypto_exchage.start()

# while True:
#     print("Kraken ", list(websock.get_data())[0])
#     print("Binance", )
