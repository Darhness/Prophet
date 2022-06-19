
import csv

from models.assetKline import ASSET_KLINE_FIELDS, AssetKline


Klines = list[AssetKline]


class KlineUtility:
    @staticmethod
    def readFromCsv(filePath: str) -> Klines:
        pass

    @staticmethod
    def writeToCsv(filePath: str, klines: Klines):
        with open("{}.csv".format(filePath), 'a', encoding="UTF8", newline='') as f:

            klinesAsDict = []
            for item in klines:
                klinesAsDict.append(item.__dict__)

            writer = csv.DictWriter(f, fieldnames=ASSET_KLINE_FIELDS)
            writer.writeheader()
            writer.writerows(klinesAsDict)

    @staticmethod
    def comressToDictionary(klines: Klines) -> dict:
        return {
            "open": [n.open for n in klines],
            "high": [n.high for n in klines],
            "low": [n.low for n in klines],
            "close": [n.close for n in klines],
            "volume": [n.volume for n in klines],
            "isClosed": [n.isClosed for n in klines],
            "startTime": [n.startTime for n in klines],
            "closeTime": [n.closeTime for n in klines]
        }
