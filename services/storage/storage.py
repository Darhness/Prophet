import queue
from typing import List
from services.exchange.models.assetKline import AssetKline

from services.storage.observer import SocketObserverSubscriber, StorageObserver


class Storage(StorageObserver, SocketObserverSubscriber):

    def __init__(self, klineHistory: List[AssetKline] = None, queueLength: int = 200) -> None:
        super().__init__()
        self.queue = queue.Queue(queueLength)

        self.fillQueue(klineHistory)

    def appendQueue(self, kline: AssetKline):
        if(self.queue.full()):
            self.queue.get()

        self.queue.put(kline)

    def fillQueue(self, klines: List[AssetKline]):
        for kline in klines:
            self.appendQueue(kline)

    def update(self, kline: AssetKline):
        if(kline.isClosed):
            self.appendQueue(kline)
            self.notify()

    def notify(self):
        for subsciber in self.observers:
            queueAsList = list(self.queue.queue)
            subsciber.update(queueAsList)
