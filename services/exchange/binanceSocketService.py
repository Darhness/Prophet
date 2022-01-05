import websocket
from threading import Thread
from websocket import WebSocketApp

from services.exchange.models.assetCode import AssetCode
from services.exchange.models.timeFrame import TimeFrame


class BinanceSocketServiceFactory():
    BASE_URL = "wss://stream.binance.com:9443/ws/"

    @staticmethod
    def klineSocketClient(assetCode: AssetCode, tradePair: AssetCode, timeFrame: TimeFrame, onMessage, onClose) -> websocket.WebSocketApp:
        market = "{}{}".format(assetCode.value, tradePair.value).lower()
        url = "{0}{1}@kline_{2}".format(
            BinanceSocketServiceFactory.BASE_URL, market, timeFrame.value)

        return WebSocketApp(url, on_message=onMessage, on_close=onClose)


class BackgroundWebsocketConnection(Thread):
    def __init__(self, socketService: WebSocketApp) -> None:
        super().__init__()
        self.socketService = socketService
        self.daemon = True

    def run(self):
        self.socketService.run_forever()

    def stop(self):
        self.socketService.close()
