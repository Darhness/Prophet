import numpy as np
import talib as ta
from typing import List

from services.exchange.models.assetKline import AssetKline


class TalibCompatible:
    def __init__(self) -> None:
        self.open = None
        self.close = None
        self.high = None
        self.low = None
        self.volume = None

    def __str__(self) -> str:
        string = ""
        for index in range(len(self.close)):
            string += "Open:{:.2f}\tHigh:{:.2f}\tLow:{:.2f}\tClose:{:.2f}\tVolume:{:.2f}\n".format(
                self.open[index], self.high[index], self.low[index], self.close[index], self.volume[index])

        return string


class TechnicalAnalysis:

    @staticmethod
    def convertToTalibCompatible(klines: List[AssetKline]) -> TalibCompatible:
        result = TalibCompatible()

        # TODO code smell
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

        result.close = np.asanyarray(close)
        result.open = np.asanyarray(open)
        result.high = np.asanyarray(high)
        result.low = np.asanyarray(low)
        result.volume = np.asanyarray(volume)

        return result

    @staticmethod
    def getRSI(data: np.ndarray, length):
        # TODO - Optimize calculation by resizing the data array. Instead of calculating all RSI's, use only the last 'length'
        if(data.size < length):
            return None

        return ta.RSI(data, timeperiod=length)[-1]
