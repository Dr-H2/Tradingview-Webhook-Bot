"""
East Village Trading Robot
Requirements: Tradingview - Alpaca - Ngrok - AWS (amazon web server)
Enter your alpaca api key and secret key in config.py
Visit the wiki on the github page for detailed installation steps

Author: Dan Wallace
Contributors: William Bracken, Brent Richmond
Website: www.brick.technology
Email: danwallaceasu@gmail.com
Created: 08/30/20

<<Last Update: 09/25/20>>

Forked contributor: Dr. H
Real Life Trading UK co-Founder
Website: reallifetrading.co.uk
Created Oct 2 2021
"""
import os
import ast
import requests
import json
import logging
from flask import Flask, request, abort
from config import *
from logging.handlers import RotatingFileHandler
from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *
from datetime import datetime

def placeOrder_alpaca(data):  
    BASE_URL = "https://paper-api.alpaca.markets"
    ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
    ORDERS_URL = "{}/v2/orders".format(BASE_URL)
    HEADERS = {'APCA-API-KEY-ID': key, 'APCA-API-SECRET-KEY': secretKey}
    order = requests.post(ORDERS_URL, json=data, headers=HEADERS)
    return json.loads(order.content)

def placeOrder_binance(data, client):
    if data["side"]=="buy":
        SIDE=OrderSide.BUY
    else:
        SIDE=OrderSide.SELL

    client.post_order(symbol=data["symbol"], side=SIDE, ordertype=OrderType.MARKET, quantity=data["qty"])

    
    #IGNORE type and time_in_force for the moment.

def webhookParse(webhook_data):
    data = ast.literal_eval(webhook_data)
    return data

def alpaca_parse(data):
    out = dict()
    out["symbol"] = data["symbol"]
    out["qty"] = data["qty"]
    out["side"] = data["side"]
    out["type"] = data["type"]
    out["time_in_force"] = data["time_in_force"]
    return out

def log_alpaca(data, logger):
    #logger.info('Alert:' + str(data))
    logger.info('Sending order: Symbol ' + data["symbol"] + ' Quantity: ' + data["qty"] + ' Buy/Sell: ' + data["side"] + ' Type: ' + data["type"] + ' Time in force: ' + data["time_in_force"])
    logger.info(' ---- Order Sent\n')

def log_binance(data, logger):
    #logger.info('Alert:' + str(data))
    logger.info('Sending order: Symbol ' + data["symbol"] + ' Quantity: ' + data["qty"] + ' Buy/Sell: ' + data["side"] + ' Type: ' + data["type"] + ' Time in force: ' + data["time_in_force"])
    logger.info(' ---- Order Sent\n')





flaskServer = Flask(__name__)

@flaskServer.route('/')
def root():
    return 'online'

@flaskServer.route('/webhook', methods=['POST'])
def webhookListen():
    if request.method == 'POST':
        data = webhookParse(request.get_data(as_text=True))
        
        # Order Logging
        log_path = 'order.log'
        #os.makedirs(log_path, exist_ok=True)
        _logger = logging.getLogger("Orders")
        _logger.setLevel(logging.INFO)

        handler = RotatingFileHandler(log_path, maxBytes=1024*1024*20, backupCount=5)
        _logger.addHandler(handler)

        # First message from a Flask worker
        _logger.info("\n============================================")
        _logger.info(str(datetime.now()) + " Flask Worker initialized")

        # Read token
        f = open("token", "r")
        token = f.read().strip("\n\r")
        f.close()

        
        # Verify token
        try:
            if token != data["token"]:
                _logger.error("token mismatch")
                _logger.error("received token is:" + data["token"])
                abort(400)
        except e:
            _logger.error(str(e))
            abort(400)

        
        
        # Place order
        if data["broker"].lower() == "alpaca":
            _logger.info("Sending Order to Alpaca...")
            order_data = alpaca_parse(data)
            log_alpaca(data, _logger)
            placeOrder_alpaca(order_data)
        else:
            _logger.info("Sending Order to Binance...")
            request_client = RequestClient(api_key=binance_key, secret_key=binance_secret, server_url="https://testnet.binance.com")
            log_binance(data, _logger)
            placeOrder_binance(data, request_client)
        
        return '', 200
    else:
        abort(400)



#key = os.environ.get("APCA_KEY")
#secretKey = os.environ.get("APCA_SECRET_KEY")
if __name__ == '__main__':
    flaskServer.run()

