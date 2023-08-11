import sys
from kraken.wsbook import WsbookKraken
from binance_exchange.wsbook import WsbookBinance


print(sys.argv)
if len(sys.argv) < 3:
    print("Usage: %s symbol depth" % sys.argv[0])
    print("Example: %s xbt/usd 10" % sys.argv[0])
    sys.exit(1)

websock = WsbookKraken(sys.argv)
bwebsocm = WsbookBinance()

while True:
    print("Kraken ", list(websock.get_data())[0])
    print("Binance", bwebsocm.connect())
