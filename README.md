# Tradingview-Alpaca-Binance connection server

Hello algo traders! This is the code for a simple server that takes Tradingview Webhooks and send orders to either Alpaca or Binance for automation. If you are familiar with setting up Flask and cloud servers like AWS, you know what to do next. This came from a fork but I made a bit of enhancement (especially by adding Binance connection option). The original repo:
https://github.com/wallacewd/Alpaca-TradingView-Trading-Bot-for-AWS. 

The code might be a little bit quick-and-dirty. If there is any problem, I apologize. It is currently used for a private purpose, but if the demand rises, I could modify it into a more mature version.

Notes: 
1. Need to install binance-futures library (pip install binance-futures)
2. Need to generate token before deploying (chmod +x generate_token.sh; ./generate_token.sh)
3. Need to have a config.py. (echo key="....(YOUR APCA KEY)..."\; secret_key="...(YOUR APCA SECRET)..."\; binance_key="...(YOUR BINANCE KEY)..."\; binance_secret="...(YOUR BINANCE SECRET)..." > config.py)
