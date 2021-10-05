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
import json
import logging
import requests
from flask import Flask, request, abort
from config import *
from logging.handlers import RotatingFileHandler
'''
from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *
'''
from datetime import datetime

from log_handler.log_handler import *
from broker_handler.alpaca_handler import *
from broker_handler.binance_handler import *



def webhookParse(webhook_data):
    data = ast.literal_eval(webhook_data)
    return data




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
            apca = AlpacaHandler(key, secretKey, paper=True)
            order_data = apca.order_parse(data)
            apca.log(data, _logger)
            # Flatten the positions on the given ticker
            if "flatten_before_trigger" in data and data["flatten_before_trigger"] == "true":
                apca.flatten(data["symbol"])
            # Place the order
            apca.placeOrder(order_data)
        elif data["broker"].lower() == "binance":
            binance = BinanceHandler(binance_key, binance_secret, testnet=True)
            binance.log(data, _logger)
            # Flatten the positions on the given ticker
            if "flatten_before_trigger" in data and data["flatten_before_trigger"] == "true":
                binance.flatten(data["symbol"])
            # Place the order
            binance.placeOrder(data)

        return '', 200
    else:
        abort(400)



#key = os.environ.get("APCA_KEY")
#secretKey = os.environ.get("APCA_SECRET_KEY")
if __name__ == '__main__':
    flaskServer.run()
