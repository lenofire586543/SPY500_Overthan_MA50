import yfinance as yf
from finviz.screener import Screener
import pandas as pd
from tqdm import tqdm

import matplotlib.pyplot as plt

pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)

filter = ['idx_sp500']#找出500的股票
stock_list = Screener(filters = filter ,table ='Performance',order='Price')

ticker_table =pd.DataFrame(stock_list.data)
ticker_list = ticker_table['Ticker'].to_list()
S_500=len(ticker_table.axes[0])
d={}
f={}
def stock_filter(df):#判定標普500成分股中有多少個股在50天線以上
    df['SMA50'] = df['Close'].rolling(window=50).mean()
    df['Criteria1'] = df['Close']>df['SMA50']
    df['Fullilment'] = df[['Criteria1']].all(axis='columns')
    return df[['Date','Fullilment']]


for ticker_string in tqdm(ticker_list):
    ticker = yf.Ticker(ticker_string)
    d[ticker_string]=ticker.history(period='3y').reset_index()
    f=pd.concat(d)

new=stock_filter(f)
#print(new)
#(df1['Math_score'] /
 #                 df1['Math_score'].sum()) * 100
ans=(new.groupby(['Date'], as_index=False).sum())
ans_index=ans.set_index(['Date'])

ans_new=ans_index['Fullilment']/S_500*100

lines=ans_new.plot.line(title='S&P500_MA50')
plt.show()

