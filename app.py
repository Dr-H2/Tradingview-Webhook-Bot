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
from binance.client import Client
from binance.enums import *

def placeOrder_alpaca(data):  
    BASE_URL = "https://paper-api.alpaca.markets"
    ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
    ORDERS_URL = "{}/v2/orders".format(BASE_URL)
    HEADERS = {'APCA-API-KEY-ID': key, 'APCA-API-SECRET-KEY': secretKey}
    order = requests.post(ORDERS_URL, json=data, headers=HEADERS)
    return json.loads(order.content)

def placeOrder_binance(data,client):
    
    if data["side"]=="buy":
        SIDE=SIDE_BUY
    else:
        SIDE=SIDE_SELL

    order = client.create_margin_order(
            symbol=data["symbol"],
            side=SIDE,
            type=ORDER_TYPE_MARKET,
            timeInForme=TIME_IN_FORCE_GTC,
            quantity=data["qty"],
            )

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

def log_alpaca(data):
    logger.info(' ---- Tradingview Alert Received')
    logger.info('Alert:' + str(data))
    logger.info(' ---- Sending Trade to Alpaca')
    logger.info('Sending order: Symbol ' + data["symbol"] + ' Quantity: ' + data["qty"] + ' Buy/Sell: ' + data["side"] + ' Type: ' + data["type"] + ' Time in force: ' + data["time_in_force"])
    logger.info(' ---- Order Sent\n')

def log_binance(data):
    logger.info(' ---- Tradingview Alert Received')
    logger.info('Alert:' + str(data))
    logger.info(' ---- Sending Trade to Binance')
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
        
        # Verify token
        try:
            if token != data["token"]:
                abort(400)
        except:
            abort(400)

        
        
        # Place order
        if data["broker"].low() == "alpaca":
            order_data = alpaca_parse(data)
            log_alpaca(data)
            placeOrder_alpaca(order_data)
        else:
            log_binance(data)
            placeOrder_binance(data, client)
        
        return '', 200
    else:
        abort(400)



#key = os.environ.get("APCA_KEY")
#secretKey = os.environ.get("APCA_SECRET_KEY")
if __name__ == '__main__':
    # Order Logging
    log_path = 'order.log'
    #os.makedirs(log_path, exist_ok=True)
    logger = logging.getLogger("Orders")
    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler(log_path, maxBytes=1024*1024*20, backupCount=5)
    logger.addHandler(handler)

    # Read token
    f = open("token", "r")
    token = f.read()
    f.close()

    client = Client(binance_key, binance_secret, testnet=True)
    flaskServer.run()

