import json

from services.exchange.binanceService import AssetCode, BinanceService, TimeFrame
from services.exchange.binanceSocketService import BinanceWebSocketClientFactory
from services.exchange.models.assetKline import AssetKline
from services.storage.storage import Storage
from strategies.rsiStrategy import RsiStrategy, RsiStrategySettings

STORAGE_LENGTH = 200

rsiStrategySettings = RsiStrategySettings(length=14, buy=25, sell=40)
strategy = RsiStrategy(rsiStrategySettings)

klineHistory = BinanceService.getKlineForAsset(
    AssetCode.BTC, AssetCode.USDT, TimeFrame.oneMinute, STORAGE_LENGTH)

storage = Storage(klineHistory)
storage.attach(strategy)


def onClose(ws):
    print("Closed")


def convertThanNotify(*values: object):
    response = values[1]
    jsonResponse = json.loads(response)

    convertedResponse = AssetKline.fromBinanceSocketResponse(jsonResponse)
    storage.update(convertedResponse)


socketClient = BinanceWebSocketClientFactory.createKlineWebSocketClient(
    AssetCode.BTC, AssetCode.USDT, TimeFrame.oneMinute, convertThanNotify, onClose)

socketClient.run_forever()
