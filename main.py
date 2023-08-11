import sys
from arbitrage_trading.crypto_exchanges import CryptoExchanges


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
