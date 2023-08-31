import websocket


class WsbookBinance:
    def __init__(self, ticker):
        self.socket = f"wss://stream.binance.com:9443/ws/{ticker}@bookTicker"

    def b_connect(self, arbitrage_watcher, on_close):
        try:
            print(arbitrage_watcher)
            ws = websocket.WebSocketApp(self.socket, on_message=arbitrage_watcher, on_close=on_close)
            print(ws.has_errored)
            ws.run_forever()
        except Exception as e:
            print(str(e))
