from binance.client import Client
from services.exchange.binanceConfig import BINANCE_API_KEY, BINANCE_SECRET_KEY
from services.exchange.models.assetKline import AssetKline

# This is pre-selected date, in order to keep data consistent.
# USDT shown a lot of divergence from 1$ before this date.
INIT_YEAR_IN_EPOCH_MILLISEC = 1535760001000

Klines = list[AssetKline]


class AssetKlineHistoryRetriever:
    """ 
    Class that helps to collect and save historical data of any asset from the Binance database.
    """

    def __init__(self, binanceClient: Client) -> None:
        self.binanceClient = binanceClient

    def getHistory(self, symbol: str, interval: str, fromDateInEpochMillisec: int = INIT_YEAR_IN_EPOCH_MILLISEC) -> Klines:
        """
        Args
        ---
        symbol : str
            Symbol made out of two assets codes that are listed on Binance.
            Example: Bitcoin 'BTC' and Thether 'USDT' would be 'BTCUSDT'
        interval : str
            Determines the time interval a closed candle is formed.
            Use the pre-defined intervals from binance.client.Client.KLINE_INTERVAL_***.\
            Example: binance.client.Client.KLINE_INTERVAL_30MINUTE
        fromDateInEpochMillisec : int
            Records will be retrieved from this date.

        Returns:
        ---
        A list of AssetKline records starting from fromDateInEpochMillisec until now.
        """
        klines: list[AssetKline] = []

        while True:
            response = self.binanceClient.get_historical_klines(
                symbol, interval, fromDateInEpochMillisec)

            if(len(response) <= 0):
                break

            for item in response:
                klines.append(AssetKline.fromBinanceApiResponse(item))

            fromDateInEpochMillisec = klines[-1].closeTime

        return klines


if __name__ == "__main__":
    selectedSymbol = "BTCUSDT"
    selectedInterval = Client.KLINE_INTERVAL_30MINUTE

    client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)
    dataCollector = AssetKlineHistoryRetriever(client)
    klines = dataCollector.getHistory(
        "BTCUSDT", Client.KLINE_INTERVAL_30MINUTE)

    AssetKline.saveToCsv("{}_{}".format(selectedSymbol, selectedInterval), klines)
