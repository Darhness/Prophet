from typing import List

from services.exchange.models.assetKline import AssetKline


class SocketObserverSubscriber:
    #TODO - GENERIC
    def update(self, kline: AssetKline):
        pass


class StorageObserverSubscriber:
    def __init__(self, length) -> None:
        self.length = length

    def update(self, klines: List[AssetKline]):
        pass


class StorageObserver:
    def __init__(self) -> None:
        self.observers: List[StorageObserverSubscriber] = []

    def attach(self, observer: StorageObserverSubscriber, length: int):
        pass

    def detach(self, observer: StorageObserverSubscriber):
        self.observers.remove(observer)

    def notify(self):
        pass
