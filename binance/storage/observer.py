from models.assetKline import AssetKline

Klines = list[AssetKline]


class SocketObserverSubscriber:
    def update(self, kline: AssetKline):
        pass


class StorageObserverSubscriber:
    def update(self, klines: Klines):
        pass


class StorageObserver:
    def __init__(self) -> None:
        self.observers: list[StorageObserverSubscriber] = []

    def attach(self, observer: StorageObserverSubscriber):
        self.observers.append(observer)

    def detach(self, observer: StorageObserverSubscriber):
        self.observers.remove(observer)

    def notify(self):
        pass
