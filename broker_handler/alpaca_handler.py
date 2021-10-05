import requests

class AlpacaHandler():
    def __init__(self, key, secret):
        self._key = key
        self._secret = secret

    def placeOrder(self, data):
        BASE_URL = "https://paper-api.alpaca.markets"
        ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
        ORDERS_URL = "{}/v2/orders".format(BASE_URL)
        HEADERS = {'APCA-API-KEY-ID': self._key, 'APCA-API-SECRET-KEY': self._secret}
        order = requests.post(ORDERS_URL, json=data, headers=HEADERS)
        return json.loads(order.content)

    def flatten_alpaca(self, symbol, client):
        pass

    def order_parse(self, data):
        out = dict()
        out["symbol"] = data["symbol"]
        out["qty"] = data["qty"]
        out["side"] = data["side"]
        out["type"] = data["type"]
        out["time_in_force"] = data["time_in_force"]
        return out

    def log(self, data, logger):
        #logger.info('Alert:' + str(data))
        logger.info('Sending order: Symbol ' + data["symbol"] + ' Quantity: ' + data["qty"] + ' Buy/Sell: ' + data["side"] + ' Type: ' + data["type"] + ' Time in force: ' + data["time_in_force"])
        logger.info(' ---- Order Sent\n')
