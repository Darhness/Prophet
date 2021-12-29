import requests
from enum import Enum

from services.exchange.models.assetKline import AssetKline
from services.exchange.models.assetCode import AssetCode
from services.exchange.models.timeFrame import TimeFrame

from services.exchange.exchange import Exchange


class BinanceService(Exchange):
    def __init__(self, authToken):
        self.authToken = authToken
        self.BASE_URL = "https://api.binance.com/api/v3/"

    def buy() -> bool:
        pass

    def sell() -> bool:
        pass

    def getWallet():
        pass

    def getOrders():
        pass

    # https://binance-docs.github.io/apidocs/spot/en/#kline-candlesTimeFrame-data
    def getKlineForAsset(self, code: AssetCode, codePair: AssetCode, TimeFrame: TimeFrame, limit) -> list[AssetKline]:
        klineUrl = self.BASE_URL + \
            "klines?symbol={}&interval={}&limit={}".format(
                code.value+codePair.value, TimeFrame.value, limit)

        response = requests.get(klineUrl).json()
        result = []

        for item in response:
            kline = AssetKline(
                open=item[1], high=item[2], low=item[3], close=item[4],  volume=item[5], isClosed=True)
            result.append(kline)

        return result
