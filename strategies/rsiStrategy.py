import json
import queue
from services.exchange.models.assetKline import AssetKline
from strategies.stategyBase import StrategyBase

"""
RSI_LENGTH = 14
RSI_BUY = 25
RSI_SELL = 25
timeFrame = 15m

LISTENING_SIGNAL = RSI == 25
buySignal = (RSI < 25) AND (FIRST GREEN VOLUME) 
sellSignal = 
    RSI == 40
    OUT on 1%?


sellSignal should be based on volume!
"""


class RsiStrategy(StrategyBase):
    def __init__(self, length, buy, sell) -> None:
        super().__init__()
        self.RSI_LENGTH = length
        self.RSI_BUY = buy
        self.RSI_SELL = sell
        self.queue = queue.Queue(self.RSI_LENGTH)

    def update(self, data):
        kline = self.convertToKline(data)
        self.preprocess(kline)

    def preprocess(self, kline: AssetKline):
        if(kline.isClosed):
            self.queue.put(kline)
            self.checkForSignal()
            self.queue.get()

    def checkForSignal(self):
        klineHistoy = list(self.queue.queue)
        rsi = 0

        if(rsi <= self.RSI_BUY):
            self.onBuySignal()

        if(rsi >= self.RSI_SELL):
            self.onSellSignal()

    def onBuySignal(self):
        inPosition = False

        if(inPosition):
            pass

    def onSellSignal(self):
        inPosition = False

        if(inPosition):
            pass
