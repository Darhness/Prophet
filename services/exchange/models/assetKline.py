from datetime import datetime


class AssetKline:
    def __init__(self, open, high, low, close, volume, isClosed, startTime, closeTime) -> None:
        self.open = float(open)
        self.high = float(high)
        self.low = float(low)
        self.close = float(close)
        self.volume = float(volume)
        self.isClosed = isClosed
        self.startTime = startTime
        self.closeTime = closeTime

    def __str__(self):
        unixTimeStamp = int(self.closeTime)
        parsedClosedTime = datetime.fromtimestamp(
            unixTimeStamp / 1000).strftime("%H:%M")

        return "CloseTime:{}\tOpen:{}\tHigh:{}\tLow:{}\tClose:{}\tVolume:{}\tisClosed:{}\n".format(parsedClosedTime, self.open, self.high, self.low, self.close, self.volume, self.isClosed)
