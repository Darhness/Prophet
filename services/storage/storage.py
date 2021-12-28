import queue
from services.exchange.models.assetKline import AssetKline

from services.storage.observer import SocketObserverSubscriber, StorageObserver, StorageObserverSubscriber


class Storage(StorageObserver, SocketObserverSubscriber):
    def __init__(self) -> None:
        super().__init__()
        self.queue = queue.Queue(100)

    def update(self, kline: AssetKline):
        if(kline.isClosed):
            self.appendQueue(kline)
            self.notify()

    def appendQueue(self, kline: AssetKline):
        # TODO
        if(self.queue.full()):
            self.queue.get()

        self.queue.put(kline)

    def notify(self):
        for subsciber in self.observers:
            queueAsList = list(self.queue.queue)
            subsciber.update(queueAsList[-subsciber.length:])

    def attach(self, observer: StorageObserverSubscriber):
        self.observers.append(observer)
        self.queue.maxsize = max(self.queue.maxsize, observer.length)
