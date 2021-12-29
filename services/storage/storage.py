import queue
from typing import List
from services.exchange.models.assetKline import AssetKline

from services.storage.observer import SocketObserverSubscriber, StorageObserver, StorageObserverSubscriber


class Storage(StorageObserver, SocketObserverSubscriber):
    DEFAULT_QUEUE_LENGTH = 200

    def __init__(self, klineHistory: List[AssetKline] = None) -> None:
        super().__init__()
        queueLength = len(klineHistory)
        self.queue = queue.Queue(max(queueLength, self.DEFAULT_QUEUE_LENGTH))

        for kline in klineHistory:
            self.appendQueue(kline)

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
            subsciber.update(queueAsList)

    def attach(self, observer: StorageObserverSubscriber):
        self.observers.append(observer)
        self.queue.maxsize = max(self.queue.maxsize, observer.length)
