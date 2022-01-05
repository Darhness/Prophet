import websocket
from threading import Thread
from websocket import WebSocketApp

from services.exchange.models.assetCode import AssetCode
from services.exchange.models.timeFrame import TimeFrame


class BinanceSocketServiceFactory():
    """ 
    Factory that helps creating websocket.WebSocketApp clients towards Binance.
    """
    BASE_URL = "wss://stream.binance.com:9443/ws/"

    @staticmethod
    def klineSocketClient(assetCode: AssetCode, tradePair: AssetCode, timeFrame: TimeFrame, onMessage, onClose) -> websocket.WebSocketApp:
        """Creates a websocket.WebSocketApp connected to the specified Binance socket service.

        Args
        ---
        assetCode : AssetCode
            Asset code to monitor.
        tradePair : AssetCode
            Asset pair to make a symbol from.
        timeFrame : TimeFrame
            Determines the time frame a closed candle is formed.
        onMessage
            Method to call when the socket client receives a message.
        onClose
            Method to call when the socket client closes.

        Returns:
        ---
        websocket.WebSocketApp connected to Binance that is ready to receive kline data.
        Use websocket.WebSocketApp.run_forever() to start execution.
        """
        market = "{}{}".format(assetCode.value, tradePair.value).lower()
        url = "{0}{1}@kline_{2}".format(
            BinanceSocketServiceFactory.BASE_URL, market, timeFrame.value)

        return WebSocketApp(url, on_message=onMessage, on_close=onClose)


class BackgroundWebsocketConnection(Thread):
    """ 
    Thread that enables running multiple socket clients in parallel.

    Attributes:
    ---
    socketService: WebSocketApp
        Socket client.
    """

    def __init__(self, socketService: WebSocketApp) -> None:
        super().__init__()
        self.socketService = socketService
        self.daemon = True

    def run(self):
        """
        Starts running the socket client in the background.
        """
        self.socketService.run_forever()

    def stop(self):
        """
        Stops the running the socket client.
        """
        self.socketService.close()
