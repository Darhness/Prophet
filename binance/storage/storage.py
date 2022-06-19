import queue

from models.assetKline import AssetKline

from observer import SocketObserverSubscriber, StorageObserver

Klines = list[AssetKline]


class Storage(StorageObserver, SocketObserverSubscriber):

    def __init__(self, klineHistory: Klines = None, queueLength: int = 200) -> None:
        super().__init__()
        self.queue = queue.Queue(queueLength)

        self.fillQueue(klineHistory)

    def appendQueue(self, kline: AssetKline):
        if(self.queue.full()):
            self.queue.get()

        self.queue.put(kline)

    def fillQueue(self, klines: Klines):
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
