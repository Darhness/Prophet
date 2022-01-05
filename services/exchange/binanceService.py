import requests

from services.exchange.binanceConfig import BINANCE_API_URL
from services.exchange.models.assetKline import AssetKline
from services.exchange.models.assetCode import AssetCode
from services.exchange.models.timeFrame import TimeFrame

from services.exchange.exchange import Exchange


class BinanceService(Exchange):
    """ 
    APIs that enables communications towards Binance.
    """
    BASE_URL = BINANCE_API_URL

    def __init__(self, authToken):
        self.authToken = authToken

    def buy():
        pass

    def sell():
        pass

    def getWallet():
        pass

    def getOrders():
        pass

    @staticmethod
    def getKlineForAsset(code: AssetCode, tradePair: AssetCode, TimeFrame: TimeFrame, limit: int) -> list[AssetKline]:
        url = BinanceService.BASE_URL + \
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
