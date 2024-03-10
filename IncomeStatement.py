import yfinance as yf
import pandas as pd

class Income_Statement:
    
    def __init__(self,ticker):
      self.ticker = ticker

    def ShowIncomeStatement(self):
       
       return self.ticker.income_stmt.T
