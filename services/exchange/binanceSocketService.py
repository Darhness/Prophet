from typing import List
from websocket import create_connection
from threading import Thread
import abc
import json
import time

import websocket
from websocket import WebSocketApp

from models.assetCode import AssetCode
from models.timeFrame import TimeFrame
from models.assetKline import AssetKline


class BinanceSocketServiceFactory():
    BASE_URL = "wss://stream.binance.com:9443/ws/"

    @staticmethod
    def klineSocketClient(assetCode: AssetCode, tradePair: AssetCode, timeFrame: TimeFrame, onMessage, onClose) -> websocket.WebSocketApp:
        market = "{}{}".format(assetCode.value, tradePair.value).lower()
        url = "{0}{1}@kline_{2}".format(
            BinanceSocketServiceFactory.BASE_URL, market, timeFrame.value)

        return WebSocketApp(url, on_message=onMessage, on_close=onClose)


class ObserverSubscriber:
    def update(self, data):
        pass


class Observer:
    def __init__(self) -> None:
        self.observers: List[ObserverSubscriber] = []

    def attach(self, observer: ObserverSubscriber):
        self.observers.append(observer)

    def detach(self, observer: ObserverSubscriber):
        self.observers.remove(observer)

    def notify(self, data):
        for observer in self.observers:
            observer.update(data)


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
    class ConsoleSub(ObserverSubscriber):
        def update(self, data):
            print(data)

    def onClose(ws):
        print("Closed")

    def convertThanNotify(*values: object) -> AssetKline:
        response = values[1]
        jsonResponse = json.loads(response)
        convertedResponse = AssetKline(jsonResponse['k']['o'], jsonResponse['k']["h"],
                                       jsonResponse['k']["l"], jsonResponse['k']["c"], jsonResponse['k']["v"], jsonResponse['k']['x'])
        print(convertedResponse)

    observer = Observer()
    consoleSub = ConsoleSub()
    observer.attach(consoleSub)

    client = BinanceSocketServiceFactory.klineSocketClient(
        AssetCode.BTC, AssetCode.USDT, TimeFrame.oneMinute, convertThanNotify, onClose)

    client.run_forever()
