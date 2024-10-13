from helpers import Trade
import yfinance as yf
import pandas as pd
import numpy as np
import json
import sys
import os

# --------------------------------------------------------------------------------------------------------------------------------------
# loading and cleaning data
if os.path.exists("data.csv"):
    df = pd.read_csv("data.csv", index_col=0)
else:
    gold_ticker = yf.Ticker("NQ=F")
    df = gold_ticker.history(period="max", interval='1h')
    df.to_csv("data.csv")

df.index = pd.to_datetime(df.index, utc=True)

df.drop(columns=['Volume', 'Dividends', 'Stock Splits'], inplace=True)

# --------------------------------------------------------------------------------------------------------------------------------------
# exit if there is missing data
bool_df = df.isna()
if not bool_df.loc[(bool_df['Close'] == True) | (bool_df['High'] == True) | (bool_df['Low'] == True) | (bool_df['Open'] == True)].empty:
    print("There is missing data")
    sys.exit("There is missing data")

with open('params.json', 'r') as file:
    data = json.load(file)

PARAMS = (
    data['WINDOW'],
    data['SIGNALS'],
    data['LOWER_PRICE_DEVIATION'],
    data['HIGHER_PRICE_DEVIATION'],
    data['POSITIONS_NATURE'],
    data['POSITIONS_SHORTCUT'],
)

# --------------------------------------------------------------------------------------------------------------------------------------
# needed cols
df['Mean'] = df['Close'].rolling(window=PARAMS['WINDOW']).mean()
df['STD'] = df['Close'].rolling(window=PARAMS['WINDOW']).std()
df['Z-Score'] = np.where(
    abs(df['High'] - df['Mean'])  > abs(df['Mean'] - df['Low']),
    (df['High'] - df['Mean']) / df['STD'],
    (df['Low'] - df['Mean']) / df['STD']
)

df['Mean'] = df['Mean'].shift(1)
df['STD'] = df['STD'].shift(1)
df['Z-Score'] = df['Z-Score'].shift(1)

df.dropna(inplace=True)

# --------------------------------------------------------------------------------------------------------------------------------------
# Buy/Sell signals
price_deviate_over_xSTD_filter = df['Z-Score'] > PARAMS['HIGHER_PRICE_DEVIATION']['ENTRY']
price_deviate_under_xSTD_filter = df['Z-Score'] < -PARAMS['LOWER_PRICE_DEVIATION']['ENTRY']

df['Signal'] = 0  # Default to hold/no position
df.loc[price_deviate_under_xSTD_filter, 'Signal'] = PARAMS['SIGNALS']['BUY'] # Buy signal
df.loc[price_deviate_over_xSTD_filter, 'Signal'] = PARAMS['SIGNALS']['SELL']  # Sell signal

# --------------------------------------------------------------------------------------------------------------------------------------
# TP/SL & trade execution

# Initialize trade tracking columns
df['Position'] = 0  # Track if we're in a trade (1 for long, -1 for short)
df['Entry_Price'] = 0.0  # Track entry price
df['Exit_Price'] = 0.0  # Track exit price
df['PnL'] = 0.0  # Track Profit and Loss for each trade

# Simulate the strategy with SL/TP
trade = Trade()

def exit_trade(idx, is_win: bool):
    df.loc[idx, 'Exit_Price'] = trade.tp if is_win else trade.sl
    pnl = trade.rrr if is_win else -1
    df.loc[idx, ['PnL', 'Position']] = [pnl, PARAMS['SIGNALS']['BUY' if trade.is_buy else 'SELL']]
    return True

def is_buy_sl(idx):
    if df.loc[idx, 'Low'] <= trade.sl: return exit_trade(idx, False)
    return False

def is_buy_tp(idx, source='High'):
    if df.loc[idx, source] > trade.tp: return exit_trade(idx, True)
    return False

def is_sell_sl(idx):
    if df.loc[idx, 'High'] >= trade.sl: return exit_trade(idx, False)
    return False

def is_sell_tp(idx, source='Low'):
    if df.loc[idx, source] < trade.tp: return exit_trade(idx, True)
    return False

# [NB] check SL first then make sure trade is On to check TP

def fill_trade_params(_row, idx):
    trade_signal = _row['Signal']

    is_long = (trade_signal == PARAMS['SIGNALS']['BUY'])

    trade.On()
    DEVIATION =  PARAMS['LOWER_PRICE_DEVIATION'] if is_long else PARAMS['HIGHER_PRICE_DEVIATION']
    trade.entry = (_row['Mean'] - trade_signal * DEVIATION['ENTRY'] * _row['STD'])
    trade.tp = (_row['Mean'] - trade_signal * DEVIATION['TP'] * _row['STD'])
    trade.sl = (_row['Mean'] - trade_signal * DEVIATION['SL'] * _row['STD'])
    df.loc[idx, ['Position', 'Entry_Price']] = [trade_signal, trade.entry]

    # check if sl or tp is already hit in the same candel (i)
    if is_long:
        if is_buy_sl(idx): trade.Off()
        elif is_buy_tp(idx, source='Close'): trade.Off()
    else:
        if is_sell_sl(idx): trade.Off()
        elif is_sell_tp(idx, source='Close'): trade.Off()

# Loop through candles and execute trades
for idx, row in df.iterrows(): # row for reading, i for writing
    if trade.on: 
        # Track price movement for Stop Loss or Take Profit
        if trade.is_buy: 
            if is_buy_sl(idx): trade.Off()
            elif is_buy_tp(idx, source='Close'): trade.Off()
        elif trade.is_sell:
            if is_sell_sl(idx): trade.Off()
            elif is_sell_tp(idx, source='Close'): trade.Off()
    else:
        if row['Signal'] != 0: # Check if there's a signal
            fill_trade_params(row, idx)

# --------------------------------------------------------------------------------------------------------------------------------------
# results

# Calculate cumulative profit/loss
df['Cumulative_PnL'] = df['PnL'].cumsum()

# Filter rows where we had a trade exit
trades = df[df['PnL'] != 0]

# Summary statistics
total_trades = len(trades)
total_pnl = df['Cumulative_PnL'].iloc[-1]  # Total profit/loss
win_rate = win_rate =(df[df['PnL'] > 0]['PnL'].count())/(df[df['PnL'] != 0]['PnL'].count())
average_RRR = df[df['PnL'] > 0]['PnL'].mean()

expectency = (average_RRR + 1) * win_rate - 1

strategy_stats_df = pd.DataFrame(
    np.array([[
        total_trades,
        total_pnl,
        round(win_rate * 100, 2),
        average_RRR,
        expectency,
        expectency * total_trades
    ]]),
    columns=['Total Trades', 'Total Profit/Loss (RR)', 'Win rate (%)', 'Average Risk-Reward Ratio', 'Expectancy', 'Expected return'],
    index=['Metrics']
)

print(strategy_stats_df)