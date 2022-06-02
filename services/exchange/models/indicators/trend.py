from services.exchange.models.assetKline import AssetKline


class Trend:
    """ 
    * MA is moving average
    """

    def __init__(self) -> None:
        self.MA20 = 0
        self.MA50 = 0
        self.MA200 = 0

    @staticmethod
    def calculate(data : list[AssetKline]):
        pass