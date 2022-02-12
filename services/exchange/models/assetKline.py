from asyncio.windows_events import NULL
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

    @staticmethod
    def fromBinanceSocketResponse(jsonResponse) -> None:
        return AssetKline(
            open=jsonResponse['k']['o'],
            high=jsonResponse['k']["h"],
            low=jsonResponse['k']['l'],
            close=jsonResponse['k']["c"],
            volume=jsonResponse['k']["v"],
            isClosed=jsonResponse['k']['x'],
            startTime=jsonResponse['k']['t'],
            closeTime=jsonResponse['k']['T']
        )

    @staticmethod
    def fromBinanceApiResponse(jsonResponse):
        return AssetKline(
            open=jsonResponse[1],
            high=jsonResponse[2],
            low=jsonResponse[3],
            close=jsonResponse[4],
            volume=jsonResponse[5],
            isClosed=True,
            startTime=jsonResponse[0],
            closeTime=jsonResponse[7]
        )

    def __str__(self):
        unixTimeStamp = int(self.closeTime)
        parsedClosedTime = datetime.fromtimestamp(
            unixTimeStamp / 1000).strftime("%H:%M")

        return "CloseTime:{}\tOpen:{}\tHigh:{}\tLow:{}\tClose:{}\tVolume:{}\tisClosed:{}\n".format(parsedClosedTime, self.open, self.high, self.low, self.close, self.volume, self.isClosed)
