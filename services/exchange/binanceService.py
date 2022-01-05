import requests

from services.exchange.models.assetKline import AssetKline
from services.exchange.models.assetCode import AssetCode
from services.exchange.models.timeFrame import TimeFrame

from services.exchange.exchange import Exchange


class BinanceService(Exchange):
    """ 
    APIs that enables communications towards Binance.
    """

    def __init__(self, authToken):
        self.authToken = authToken
        self.BASE_URL = "https://api.binance.com/api/v3/"

    def buy():
        pass

    def sell():
        pass

    def getWallet():
        pass

    def getOrders():
        pass

    def getKlineForAsset(self, code: AssetCode, tradePair: AssetCode, TimeFrame: TimeFrame, limit: int) -> list[AssetKline]:
        url = self.BASE_URL + \
            "klines?symbol={}&interval={}&limit={}".format(
                code.value+tradePair.value, TimeFrame.value, limit)

        response = requests.get(url).json()
        klines = []

        for item in response:
            kline = AssetKline(
                open=item[1],
                high=item[2],
                low=item[3],
                close=item[4],
                volume=item[5],
                isClosed=True,
                startTime=item[0],
                closeTime=item[7]
            )
            klines.append(kline)

        return klines
