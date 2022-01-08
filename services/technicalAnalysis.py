import numpy as np
import talib as ta
from typing import List

from services.exchange.models.assetKline import AssetKline


class TalibCompatible:
    def __init__(self, klines: List[AssetKline] = None) -> None:
        self.open = None
        self.close = None
        self.high = None
        self.low = None
        self.volume = None

        if klines is not None:
            self.processKlines(klines)

    def processKlines(self, klines: List[AssetKline]):
        open = []
        close = []
        high = []
        low = []
        volume = []

        for kline in klines:
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

    def __str__(self) -> str:
        string = ""
        for index in range(len(self.close)):
            string += "Open:{:.2f}\tHigh:{:.2f}\tLow:{:.2f}\tClose:{:.2f}\tVolume:{:.2f}\n".format(
                self.open[index], self.high[index], self.low[index], self.close[index], self.volume[index])

        return string


class TechnicalAnalysis:
    @staticmethod
    def getRSI(data: np.ndarray, length):
        if(data.size < length):
            return None

        return ta.RSI(data, timeperiod=length)[-1]
