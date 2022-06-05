import numpy as np
import talib as ta
from assetKlineHistoryRetriever import AssetKlineHistoryRetriever
from services.exchange.models.assetKline import AssetKline


from binance.client import Client
from services.exchange.binanceConfig import BINANCE_API_KEY, BINANCE_SECRET_KEY
from services.exchange.models.assetKline import AssetKline


class KlineTechnicalAnalyser:

    def __init__(self, klines: list[AssetKline]) -> None:
        self.klines = klines
        self.open = None
        self.close = None
        self.high = None
        self.low = None
        self.volume = None

        self.calculatedIndicators = {}

        self.__preProcess()

    def __preProcess(self):
        open = []
        close = []
        high = []
        low = []
        volume = []

        for kline in self.klines:
            open.append(float(kline.open))
            close.append(float(kline.close))
            high.append(float(kline.high))
            low.append(float(kline.low))
            volume.append(float(kline.volume))

        self.close = np.asanyarray(close)
        self.open = np.asanyarray(open)
        self.high = np.asanyarray(high)
        self.low = np.asanyarray(low)
        self.volume = np.asanyarray(volume)

    def RSI(self, length: int = 14):
        calculatedResults = ta.RSI(self.close, timeperiod=length)
        self.calculatedIndicators["RSI{}".format(length)] = calculatedResults

        return self

    def CCI(self, length: int = 14):
        calculatedResults = ta.CCI(
            self.high, self.low, self.close, timeperiod=length)
        self.calculatedIndicators["CCI{}".format(length)] = calculatedResults

        return self

    def MA(self, length: int):
        calculatedResults = ta.MA(self.close, timeperiod=length)
        self.calculatedIndicators["MA{}".format(length)] = calculatedResults

        return self

    def BOLL(self, length: int = 20):
        upper, middle, lower = ta.BBANDS(
            self.close, timeperiod=length, nbdevup=2, nbdevdn=2, matype=0)

        self.calculatedIndicators["BOLL{}-UP".format(length)] = upper
        self.calculatedIndicators["BOLL{}-MID".format(length)] = middle
        self.calculatedIndicators["BOLL{}-DOWN".format(length)] = lower

        return self

    def ATR(self, length: int = 14):
        calculatedResults = ta.ATR(
            self.high, self.low, self.close, timeperiod=length)
        self.calculatedIndicators["ATR{}".format(length)] = calculatedResults

        return self

    def get(self):
        return self.calculatedIndicators


if __name__ == "__main__":
    selectedSymbol = "BTCUSDT"
    selectedInterval = Client.KLINE_INTERVAL_8HOUR

    client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)
    dataCollector = AssetKlineHistoryRetriever(client)

    klines = dataCollector.getHistory(
        selectedSymbol, selectedInterval)

    result = KlineTechnicalAnalyser(klines).ATR(14).get()
    print(result["ATR14"][-1])
    print(result["ATR14"][-2])
