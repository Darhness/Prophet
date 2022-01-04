class AssetKline:
    def __init__(self, open, high, low, close, volume, isClosed, startTime, closeTime) -> None:
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.isClosed = isClosed
        self.startTime = startTime
        self.closeTime = closeTime

    def __str__(self):
        return "Open:{}\tHigh:{}\tLow:{}\tClose:{}\tVolume:{}\tisClosed:{}\n".format(self.open, self.high, self.low, self.close, self.volume, self.isClosed)
