import websocket


class WsbookBinance:
    def __init__(self):
        self.socket = "wss://stream.binance.com:9443/ws/btcusdt@bookTicker"

    def b_connect(self, arbitrage_watcher, on_close):
        try:
            ws = websocket.WebSocketApp(self.socket, on_message=arbitrage_watcher, on_close=on_close)
            ws.run_forever()
        except Exception as e:
            print(str(e))
