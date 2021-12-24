from os import close
from models.assetKline import AssetKline


class Exchange:
    """ 
    Required APIs that an exchange should fullfill.
    """
    def buy():
        """
        Executes a buy order.
        """
        pass

    def sell():
        """
        Executes a sell order.
        """
        pass

    def getWallet():
        """
        Retrieves the current vallet state on the exchange.
        """
        pass

    def getOrders():
        """
        Retrieves pending orders.
        """
        pass

    def getKlineForAsset(code: str, codePair: str, limit, TimeFrame) -> list[AssetKline]:
        """
        Retrieves the candlesTimeFrame data for an asset.
        """
        pass
