class AssetKline:
    def __init__(self, open, high, low, close, volume, isClosed) -> None:
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.isClosed = isClosed

    def __str__(self):
        return "Open:{} High:{} Low:{} Close:{} Volume:{} isClosed:{}\n".format(self.open, self.high, self.low, self.close, self.volume, self.isClosed)
