from services.exchange.models.assetKline import AssetKline
from services.storage.observer import StorageObserverSubscriber


class StrategyBase(StorageObserverSubscriber):
    def checkForSignal(self):
        pass

    def onBuySignal(self):
        pass

    def onSellSignal(self):
        pass
