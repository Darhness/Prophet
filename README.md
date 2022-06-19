# TradingBot

The aim of this project is to create a tool, that can help make future price predictions of stock or crypto currency assets on the market.

## Python requirements

### Common modules

    pip install pandas websocket-client numpy requests python-binance csv queue json

### TA-LIB
Talib is originally a C library that contains more than 150 trading indicator algorithm implementations. Besides the C library we also have to install a python wrapper that allowes us to use it.

1. Download the ta-lib library installer that is compatible with your Python version from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib).
    1.2 Using **pip** install the library. `pip install installer_from_first_step.whl`
2. Install the python module that enables us to use this library. `pip install ta-lib`

Install reference [here](https://www.youtube.com/watch?v=hZIZMMcTQ8c&ab_channel=MartinMayer).
Talib API helper [here](https://www.programcreek.com/python/index/7769/talib).