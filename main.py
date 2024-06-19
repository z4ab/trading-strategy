import yfinance as yf
import pandas as pd
import numpy as np
import time

symbol = 'AAPL'
buying_power = 1000  # Amount in dollars you want to allocate for trading
moving_average_period = '1mo'
buy_threshold = 0.99  # Buy when the price is 1% below the moving average
sell_threshold = 1.01  # Sell when the price is 1% above the moving average

cash = 5000
shares = 0 # How many shares you own

def get_moving_average(symbol, period):
    data = yf.download(symbol, period=period, interval='1d')
    moving_average = data['Close'].mean()
    return moving_average

def get_current_price(symbol):
    data = yf.download(symbol, period='1d', interval='1m')
    current_price = data['Close'].iloc[-1]
    return current_price

def place_order(symbol, qty, side, price):
    if (side == 'buy'):
        cash -= qty*price 
        shares += qty
    elif (side == 'sell'):
        cash += qty*price
        shares -= qty
    print(f"Placing {side} order for {qty} shares of {symbol}")

def run_trading_bot():
    while True:
        moving_average = get_moving_average(symbol, moving_average_period)
        current_price = get_current_price(symbol)
        print(f"Current Price: {current_price}, Moving Average: {moving_average}")

        if current_price <= moving_average * buy_threshold:
            qty_to_buy = int(buying_power / current_price)
            if qty_to_buy > 0:
                print(f"Placing buy order for {qty_to_buy} shares of {symbol}")
                place_order(symbol, qty_to_buy, 'buy', current_price)
        elif current_price >= moving_average * sell_threshold:
            if shares > 0:
                print(f"Placing sell order for {shares} shares of {symbol}")
                place_order(symbol, shares, 'sell', current_price)

        time.sleep(60)  # Wait for 1 minute before the next iteration

# Start the trading bot
run_trading_bot()