import numpy as np
from typing import List

from services.exchange.models.assetKline import AssetKline


class TalibCompatible:
    def __init__(self) -> None:
        self.open = None
        self.closed = None
        self.high = None
        self.low = None
        self.volume = None


class TechnicalAnalysis:

    @staticmethod
    def convertToTalibCompatible(klines: List[AssetKline]) -> TalibCompatible:
        result = TalibCompatible()

        # TODO code smell
        open = []
        closed = []
        high = []
        low = []
        volume = []

        for kline in klines:
            open.append(float(kline.open))
            closed.append(float(kline.close))
            high.append(float(kline.high))
            low.append(float(kline.low))
            volume.append(float(kline.volume))

        result.closed = np.asanyarray(closed)
        result.open = np.asanyarray(open)
        result.high = np.asanyarray(high)
        result.low = np.asanyarray(low)
        result.volume = np.asanyarray(volume)

        return result
