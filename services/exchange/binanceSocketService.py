import websocket
from threading import Thread
from websocket import WebSocketApp

from services.exchange.binanceConfig import BINANCE_SOCKET_API_URL
from services.exchange.models.assetCode import AssetCode
from services.exchange.models.timeFrame import TimeFrame

class KlineRequest:
    def __init__(self, code: AssetCode, tradePair: AssetCode, timeFrame: TimeFrame) -> None:
        self.code: AssetCode = code
        self.tradePair: AssetCode = tradePair
        self.timeFrame: TimeFrame = timeFrame
        self.limit: int = None
        self.startTime: int = None
        self.endTime: int = None

    def __str__(self) -> str:
        symbol = "&symbol={}".format(self.code.value+self.tradePair.value)        
        startTime = "" if self.startTime is None else "&startTime={}".format(self.startTime)
        endTime = "" if self.endTime is None or self.startTime is None else "&endTime={}".format(self.endTime)
        limit = "&limit={}".format(self.limit) if self.limit is not None else ""

        return "klines?{}&interval={}{}{}{}".format(symbol, self.timeFrame.value, startTime, endTime, limit)

class KlineRequestBuilder:
    def __init__(self, code: AssetCode, tradePair: AssetCode, timeFrame: TimeFrame) -> None:
        self.request = KlineRequest(code, tradePair, timeFrame)

    def limit(self, limit):
        self.request.limit = limit

        return self

    def startTime(self, startTime):
        self.request.startTime = startTime

        return self

    def dateInterval(self, startTime : int, endTime: int):
        self.request.startTime = startTime
        self.request.endTime = endTime

        return self

    def build(self):
        return self.request

class BinanceWebSocketClientFactory():
    """ 
    Factory that helps creating websocket.WebSocketApp clients towards Binance.
    """
    BASE_URL = BINANCE_SOCKET_API_URL

    @staticmethod
    def createKlineWebSocketClient(assetCode: AssetCode, tradePair: AssetCode, timeFrame: TimeFrame, onMessage, onClose) -> websocket.WebSocketApp:
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
            BinanceWebSocketClientFactory.BASE_URL, market, timeFrame.value)

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
