import websocket, json


class WsbookBinance:
    def __init__(self):
        self.bid = 0
        self.ask = 0
        self.socket = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"
        #ws = websocket.WebSocketApp(self.socket, on_message=self.on_message, on_close=self.on_close)

    def on_message(self, ws, message):
        print(message)

    def on_close(self):
        print("### Closed ###")


    def connect(self):
        ws = websocket.create_connection(self.socket)
        print(ws)
