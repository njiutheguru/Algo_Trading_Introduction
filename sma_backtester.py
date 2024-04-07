#!/usr/bin/env python
# coding: utf-8
# %%
import yfinance as yf
import pandas as pd
import numpy as np
# %matplotlib inline
import matplotlib.pyplot as plt


class SMABacktester():
    def __init__(self,symbol,sma_s, sma_l, start,end):
        self.symbol = symbol
        self.sma_s = sma_s
        self.sma_l = sma_l
        self.start = start
        self.end = end
        self.results = None
        self.get_data()
        
    def get_data(self):
        df = yf.download(self.symbol, start=self.start, end=self.end)
        data = df.Close.to_frame()
        data['returns'] = np.log(data.Close.div(data.Close.shift(1)))
        data['sma_s'] = data.Close.rolling(self.sma_s).mean()
        data['sma_l'] = data.Close.rolling(self.sma_l).mean()
        data.dropna(inplace=True)
        self.data2 = data
        
        return data
    
    
    def test_results(self):
        data = self.data2.copy().dropna()
        data["position"] = np.where(data['sma_s'] > data["sma_l"], 1,-1)
        data['strategy'] = data['returns'] * data.position.shift(1)
        data.dropna(inplace = True)
        data["returnsbh"] = data['returns'].cumsum().apply(np.exp)
        data['returns_strategy'] = data['strategy'].cumsum().apply(np.exp)
        perf = data['returns_strategy'].iloc[-1]
        outperf = perf - data['returnsbh'].iloc[-1]
        self.results = data
        
        ret = np.exp(data['strategy'].sum())
        std = data['strategy'].std() *np.sqrt(252)
        
        # return tuple ret,std
        return round(perf,6), round(outperf,6)
    
    
    def plot_results(self):
        if self.results is None:
            print("Run the test please!")
        else:
            title = "{} | sma_s = {} | sma_l = {}".format(self.symbol, self.sma_s, self.sma_l)
            self.results[["returnsbh", "returns_strategy"]].plot(title=title, figsize=(12,8))
            
        

# %%
tester = SMABacktester("SPY",50,100,"2000-01-01","2020-01-01")

# %%
tester.test_results()

# %%
tester = SMABacktester("AAPL",30,200,"2000-01-01","2020-01-01")

# %%
tester.test_results()

# %%
tester = SMABacktester("TSLA",20,50,"2000-01-01","2020-01-01")

# %%
tester.test_results()

# %%
