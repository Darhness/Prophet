from services.exchange.models.assetCode import AssetCode
from services.exchange.models.assetKline import AssetKline


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

    def getKlineForAsset(code: AssetCode, tradePair: AssetCode, limit, TimeFrame) -> list[AssetKline]:
        """
        Retrieves the candlestick data for an asset pair in a given time frame.
        """
        pass
