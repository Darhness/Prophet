from typing import List
from services.exchange.models.assetKline import AssetKline
from services.technicalAnalysis import TalibCompatible, TechnicalAnalysis
from strategies.stategyBase import StrategyBase


class RsiStrategySettings:
    def __init__(self, length, buy, sell) -> None:
        self.RSI_LENGTH = length
        self.RSI_BUY = buy
        self.RSI_SELL = sell


class RsiStrategyTechnicalAnalysis:
    def __init__(self, data: TalibCompatible, latestKline: AssetKline) -> None:
        self.RSI14 = TechnicalAnalysis.getRSI(data.close, 14)
        self.latestKline = latestKline

    def __str__(self) -> str:
        return "RSI 14: {}\nLatest kline: {}\n".format(self.RSI14, self.latestKline)


class RsiStrategy(StrategyBase):
    def __init__(self, settings: RsiStrategySettings) -> None:
        self.settings = settings

    def update(self, klines: List[AssetKline]):
        convertedKline = TalibCompatible(klines)
        processed = RsiStrategyTechnicalAnalysis(convertedKline, klines[-1])

        self.checkForSignal(processed)

    def checkForSignal(self, data: RsiStrategyTechnicalAnalysis):
        print(data)
        """
        if(rsi <= self.RSI_BUY):
            self.onBuySignal()

        if(rsi >= self.RSI_SELL):
            self.onSellSignal()
        """

    def onBuySignal(self):
        inPosition = False

        if(inPosition):
            pass

    def onSellSignal(self):
        inPosition = False

        if(inPosition):
            pass
