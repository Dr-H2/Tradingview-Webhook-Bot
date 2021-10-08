import requests
import json

APCA_SUCCESS = 0
APCA_OTHER_ERROR = 1
APCA_ORDER_PENDING = 2

class AlpacaHandler():
    def __init__(self, key, secret, paper=False):
        self._key = key
        self._secret = secret

        if paper:
            self._BASE_URL = "https://paper-api.alpaca.markets"
        else:
            self._BASE_URL = "https://api.alpaca.markets"

        self._HEADERS = {'APCA-API-KEY-ID': self._key, 'APCA-API-SECRET-KEY': self._secret}


    def placeOrder(self, data):
        ORDERS_URL = "{}/v2/orders".format(self._BASE_URL)

        order = requests.post(ORDERS_URL, json=data, headers=self._HEADERS)
        return json.loads(order.content)

    def flatten(self, symbol):
        POSITIONS_URL = "{}/v2/positions".format(self._BASE_URL)

        order = requests.delete(POSITIONS_URL+"/"+symbol, headers=self._HEADERS)
        return json.loads(order.content)


    def order_parse(self, data):
        out = dict()
        out["symbol"] = data["symbol"]
        out["qty"] = data["qty"]
        out["side"] = data["side"]
        out["type"] = data["type"]
        out["time_in_force"] = data["time_in_force"]
        return out

    def error_process(self, res):
        if "status" in res and res["status"] == "accepted":
            return APCA_SUCCESS
        if ("existing_qty" in res and res["existing_qty"] != 0) and ("message" in res and res["message"][:16]=="insufficient qty"):
            return APCA_ORDER_PENDING
        return APCA_OTHER_ERROR

    def log(self, data, logger):
        #logger.info('Alert:' + str(data))
        logger.info('Sending order: Symbol ' + data["symbol"] + ' Quantity: ' + data["qty"] + ' Buy/Sell: ' + data["side"] + ' Type: ' + data["type"] + ' Time in force: ' + data["time_in_force"])
