import json
from services.exchange.binanceSocketService import ObserverSubscriber
from services.exchange.models.assetKline import AssetKline


class StrategyBase(ObserverSubscriber):
    def checkForSignal(self):
        pass

    def onBuySignal(self):
        pass

    def onSellSignal(self):
        pass

    def convertToKline(self, data) -> AssetKline:
        response = data
        jsonResponse = json.loads(response)
        convertedResponse = AssetKline(jsonResponse['k']['o'], jsonResponse['k']["h"], jsonResponse['k']
                                       ["l"], jsonResponse['k']["c"], jsonResponse['k']["v"], jsonResponse['k']['x'])

        return convertedResponse
