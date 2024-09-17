import yfinance as yf
import os
import csv

# Remove existing file
try:
    os.remove('./data.csv')
except:
  print("No such file")

gold_ticker = yf.Ticker("GC=F")

df = gold_ticker.history(period="1y", interval='1h')

df.drop(columns=['Dividends', 'Stock Splits'], inplace=True)

df.reset_index(inplace=True)

with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    writer.writerow(list(df.columns))

    for i in range(0, len(df)):
       print(df.loc[i])
       writer.writerow(df.loc[i].values)


 