from services.exchange.models.assetKline import AssetKline


class RelativeStrengthIndex:
    pass

    def getRsi(state, klineHistory: list[AssetKline]):
        length = len(klineHistory)
        ups = []
        downs = []

        for index in (1, length):
            previousKlineIndex = index - 1
            change = klineHistory[index].close - \
                klineHistory[previousKlineIndex].close

            if(change > 0):
                ups.append(klineHistory[index])
            else:
                downs.append(klineHistory[index])

        relativeStrength = 42

        return 100 - 100 / (1 + relativeStrength)
        pass
