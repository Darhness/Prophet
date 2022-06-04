from typing import List

from services.exchange.models.assetKline import AssetKline


class SocketObserverSubscriber:
    def update(self, kline: AssetKline):
        pass

class StorageObserverSubscriber:
    def update(self, klines: List[AssetKline]):
        pass

class StorageObserver:
    def __init__(self) -> None:
        self.observers: List[StorageObserverSubscriber] = []

    def attach(self, observer: StorageObserverSubscriber):
        self.observers.append(observer)

    def detach(self, observer: StorageObserverSubscriber):
        self.observers.remove(observer)

    def notify(self):
        pass
