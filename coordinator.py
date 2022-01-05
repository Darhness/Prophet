import json

from services.exchange.binanceService import AssetCode, BinanceService, TimeFrame
from services.exchange.binanceSocketService import BinanceSocketServiceFactory
from services.exchange.models.assetKline import AssetKline
from services.storage.storage import Storage
from strategies.rsiStrategy import RsiStrategy, RsiStrategySettings

STORAGE_LENGTH = 200

rsiStrategySettings = RsiStrategySettings(length=14, buy=25, sell=40)
strategy = RsiStrategy(rsiStrategySettings)

binanceClient = BinanceService("")
klineHistory = binanceClient.getKlineForAsset(
    AssetCode.BTC, AssetCode.USDT, TimeFrame.oneMinute, STORAGE_LENGTH)

storage = Storage(klineHistory)
storage.attach(strategy)


def onClose(ws):
    print("Closed")


def convertThanNotify(*values: object):
    response = values[1]
    jsonResponse = json.loads(response)

    convertedResponse = AssetKline(
        open=jsonResponse['k']['o'],
        high=jsonResponse['k']["h"],
        low=jsonResponse['k']['l'],
        close=jsonResponse['k']["c"],
        volume=jsonResponse['k']["v"],
        isClosed=jsonResponse['k']['x'],
        startTime=jsonResponse['k']['t'],
        closeTime=jsonResponse['k']['T']
    )
    storage.update(convertedResponse)


socketClient = BinanceSocketServiceFactory.klineSocketClient(
    AssetCode.BTC, AssetCode.USDT, TimeFrame.oneMinute, convertThanNotify, onClose)

socketClient.run_forever()
