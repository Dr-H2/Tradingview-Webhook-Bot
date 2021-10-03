# Tradingview-Alpaca-Binance connection server

Hello algo traders! This is the code for a simple server that takes Tradingview Webhooks and send orders to either Alpaca or Binance for automation! If you are familiar with setting up Flask and cloud servers like AWS, you know what to do next. This is a direct fork and simple enhancement of the original repo in
https://github.com/wallacewd/Alpaca-TradingView-Trading-Bot-for-AWS

Notes: 
1. Need to install binance-futures library (pip install binance-futures)
2. Need to generate token before deploying (chmod +x generate_token.sh; ./generate_token.sh)
3. Need to have a config.py. (echo key="....(YOUR APCA KEY)..."\; secret_key="...(YOUR APCA SECRET)..."\; binance_key="...(YOUR BINANCE KEY)..."\; binance_secret="...(YOUR BINANCE SECRET)..." > config.py)

But if you need hand-in-hand help to set things up, please feel free to set up a session with Dr. H or Doc Martin from https://www.reallifetrading.co.uk/team

# Real Life Trading UK

We are a trading community that provides regular official content. Please check out https://reallifetrading.co.uk
