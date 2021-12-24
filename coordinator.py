import requests

from services.exchange.binanceService import AssetCode, BinanceService, TimeFrame


client = BinanceService("")
data = client.getKlineForAsset(
    AssetCode.BTC, AssetCode.USDT, TimeFrame.fiveMinute, 1)
for item in data:
    print(item)
