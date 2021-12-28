from typing import List
from websocket import create_connection
from threading import Thread
import json

import websocket
from websocket import WebSocketApp

from services.exchange.models.assetCode import AssetCode
from services.exchange.models.timeFrame import TimeFrame
from services.exchange.models.assetKline import AssetKline


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


if __name__ == '__main__':
    def onClose(ws):
        print("Closed")

    def convertThanNotify(*values: object) -> AssetKline:
        response = values[1]
        jsonResponse = json.loads(response)
        convertedResponse = AssetKline(jsonResponse['k']['o'], jsonResponse['k']["h"],
                                       jsonResponse['k']["l"], jsonResponse['k']["c"], jsonResponse['k']["v"], jsonResponse['k']['x'])
        print(convertedResponse)

    client = BinanceSocketServiceFactory.klineSocketClient(
        AssetCode.BTC, AssetCode.USDT, TimeFrame.oneMinute, convertThanNotify, onClose)

    client.run_forever()
