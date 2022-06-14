import datetime
import json
from binance.client import Client
import requests

from services.exchange.binanceConfig import BINANCE_API_KEY, BINANCE_SECRET_KEY, TIINGO_API_KEY
from services.exchange.models.assetKline import AssetKline

# This is pre-selected date, in order to keep data consistent.
# USDT shown a lot of divergence from 1$ before this date.
INIT_YEAR_IN_EPOCH_MILLISEC = 1535760001000
INIT_YEAR_IN_DATE = "2018-09-01"

TIINGO_MAX_CONTENT_LENGTH = 10000

Klines = list[AssetKline]


class AssetKlineHistoryRetriever:
    """ 
    Class that helps to collect and save historical data of any crypto/stock asset.
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

    def getStockHistory(self, symbol: str, interval: str, startDate: str = INIT_YEAR_IN_DATE, afterHours: str = "false") -> Klines:
        """
        Learn more at https://api.tiingo.com/documentation/iex.
        """
        lastRequestContentLength = TIINGO_MAX_CONTENT_LENGTH
        klines: list[AssetKline] = []
        endDate = datetime.date.today() + datetime.timedelta(days=1)

        while lastRequestContentLength == TIINGO_MAX_CONTENT_LENGTH:
            requestUrl = "https://api.tiingo.com/iex/{symbol}/prices?startDate={startDate}&endDate={endDate}&resampleFreq={timeFrame}&afterHours={afterHours}&columns=open,high,low,close,volume&token={token}".format(
                symbol=symbol, startDate=startDate, endDate=endDate, timeFrame=interval, afterHours=afterHours, token=TIINGO_API_KEY)

            requestResponse = requests.get(
                requestUrl, headers={'Content-Type': 'application/json'})
            rawCandles = json.loads(requestResponse.content)

            for candleData in rawCandles:
                klines.append(AssetKline.fromTiingoApiResponse(candleData))

            startDate = rawCandles[-1]['date']
            lastRequestContentLength = len(rawCandles)

        return klines


if __name__ == "__main__":
    """
    NOTE

    Binance history has gaps in it! Correct it if needed!
    """

    """
    selectedSymbol = "BTCUSDT"
    selectedInterval = Client.KLINE_INTERVAL_5MINUTE

    client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)
    dataCollector = AssetKlineHistoryRetriever(client)

    klines = dataCollector.getHistory(
        selectedSymbol, selectedInterval)

    """
    selectedSymbol = "SPY"
    selectedInterval = "1hour"

    client = None
    dataCollector = AssetKlineHistoryRetriever(client)

    klines = dataCollector.getStockHistory(
        selectedSymbol, selectedInterval, afterHours="true")

    AssetKline.saveToCsv("{}_{}".format(
        selectedSymbol, selectedInterval), klines)
