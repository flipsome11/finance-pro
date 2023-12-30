import datetime as dt 
import matplotlib.pyplot as plt 
from matplotlib import style
import seaborn as sns
import pandas as pd 
import yfinance as yf 
from pandas_datareader import data as pdr
import numpy as np 
import plotly.graph_objects as go

ticker = yf.Ticker('AAPL')
data = ticker.history(period="1mo", interval="1d")

print(data.isnull().sum())
data.ffill(inplace=True)
data['Daily Return'] = data['Close'].pct_change()
monthly_data = data.resample('M').mean()
data_2023 = data.loc['2023']

print(data.head())



# tickers = ('TSLA', 'AAPL', 'AMZN', 'GOOGL')
# data = yf.download(tickers, start='2018-01-01', end='2023-01-01')['Close']



# daily_returns = data.pct_change()
# volatility = daily_returns.std() * np.sqrt(252)

# data_2023 = data[data.index.year == 2023]

# print(data.columns)


# data.plot(figsize=(14,7))
# plt.title('Closing Prices of Tech Giants')
# plt.ylabel('Price ($)')
# plt.show()

# daily_returns.hist(bins=100, figsize=(14,7))
# plt.title('Histogram of Daily Returns')
# plt.show()


# print(volatility)



