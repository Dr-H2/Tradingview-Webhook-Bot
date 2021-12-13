# Tradingview-Alpaca-Binance connection server

Hello algo traders! This is the code for a simple server that takes Tradingview Webhooks and send orders to either Alpaca or Binance for automation. If you are familiar with setting up Flask and cloud servers like AWS, you know what to do next. This came from a fork but I made quite a bit of enhancements (especially by adding Binance connection option). The original repo:
https://github.com/wallacewd/Alpaca-TradingView-Trading-Bot-for-AWS. 


Usage: 
1. Need to install binance-futures library (pip install binance-futures)
2. Need to generate token before deploying (chmod +x generate_token.sh; ./generate_token.sh)
3. Need to have a config.py. (echo key="....(YOUR APCA KEY)..."\; secret_key="...(YOUR APCA SECRET)..."\; binance_key="...(YOUR BINANCE KEY)..."\; binance_secret="...(YOUR BINANCE SECRET)..." > config.py)
4. Deploy it as a Flask app. The setup varies, depending on the hosting server you choose (Heroku, GCP, AWS, private server, etc.). There are too many possibilities and variations and I cannot elaborate here.
5. Once the server is set up, it reacts to Webhooks (HTTP POST request in JSON format) that are sent to it. The workflow is the following:

```
  -------------------     Webhook     ----------      the JSON "broker" key = "alpaca"      ----------
  Tradingview Alert |     ======>     | Server |      ================================>     | Alpaca |
  -------------------                 ----------                                            ----------
                                                      the JSON "broker" key = "binance"     -----------
                                                      ================================>     | Binance |
                                                                                            -----------
```
  
  
# Sample alert message from Tradingview:
```
{ 
"token": "*************",
"broker": "binance",
"flatten_before_trigger": "true",
"symbol": "{{ticker}}", 
"qty": "{{strategy.order.contracts}}", 
"side": "{{strategy.order.action}}", 
"type": "market",
"time_in_force": "gtc" 
}
```
Notes:
1. Please use the token you generated from the script "generate_token.sh". It is saved as a plain text file "token" in the same folder (TODO: hash it).
2. It operates via pine script (strategy script instead of study) on Tradingview.
3. {{ticker}}, {{strategy.order.contracts}}, {{strategy.order.action}} are reserved for variables defined in the Tradingview strategy script. No need to change them unless you have special needs.
4. The Tradingview script does not have special requirements other than it is capable of sending out alerts. For the alert setup, please refer to the following example.

An example of the Tradingview Alert setup:

![alt text](https://cdn.discordapp.com/attachments/830931439612723221/919915047550058527/Screenshot_from_2021-12-13_06-11-59.png)

