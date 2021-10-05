from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *


class BinanceHandler():
    def __init__(self, key, secret, testnet=False):
        self._key = key
        self._secret = secret
        if testnet:
            self._client = RequestClient(api_key=key, secret_key=secret, url="https://testnet.binance.com")
        else:
            self._client = RequestClient(api_key=key, secret_key=secret, url="https://fapi.binance.com")

    def placeOrder(self, data):
        if data["side"]=="buy":
            SIDE=OrderSide.BUY
        else:
            SIDE=OrderSide.SELL

        qty = float(data["qty"])

        self._client.post_order(symbol=data["symbol"], side=SIDE, ordertype=OrderType.MARKET, quantity="{:.3f}".format(qty))
        #IGNORE type and time_in_force for the moment.

    def flatten(self, symbol):
        pos = self._client.get_position_v2()

        # Find the symbol and flatten
        for obj in pos:
            if obj.symbol == symbol:
                if obj.positionAmt > 0:
                    SIDE = OrderSide.SELL
                elif obj.positionAmt < 0:
                    SIDE = OrderSide.BUY
                if obj.positionAmt != 0.0:
                    self._client.post_order(symbol=symbol, side=SIDE, ordertype=OrderType.MARKET, quantity=abs(obj.positionAmt))
                break

    def log(self, data, logger):
        #logger.info('Alert:' + str(data))
        logger.info('Sending order: Symbol ' + data["symbol"] + ' Quantity: ' + data["qty"] + ' Buy/Sell: ' + data["side"] + ' Type: ' + data["type"] + ' Time in force: ' + data["time_in_force"])
        logger.info(' ---- Order Sent\n')
