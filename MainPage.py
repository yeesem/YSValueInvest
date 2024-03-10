import yfinance as yf
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from IncomeStatement import Income_Statement


###SIDEBAR
st.sidebar.header("Menu")
def menu():
      
      menu_option = st.sidebar.radio('Pages',
                               options = ["Main Page","Income Statement","Balance Sheet","Cash Flow"])
    
      return menu_option

menu = menu()

#User input stock symbol
key_stock_symbol = "1155.KL"
stockName = st.text_input("Stock Symbol",key = key_stock_symbol)
ticker = yf.Ticker(stockName)

###MAIN PAGE
if menu == 'Main Page':
  
  #Method for timeline sidebar
  def timeline():
    
      st.sidebar.write("Date Range Selection")
      current_date =  datetime.datetime.now().date()
      start_date = current_date - datetime.timedelta(days = 10 * 365)
      start = st.sidebar.slider("Start Date",start_date,current_date)
      end = st.sidebar.slider("End Date",start_date,current_date)
    
      chartDate = {"Start Date":start,"End Date":end}
    
      return chartDate
  
  #Diaplay timeline side bar
  df = timeline()

#   #User input stock symbol
#   key_stock_symbol = "1155.KL"
#   stockName = st.text_input("Stock Symbol",key = key_stock_symbol)
#   ticker = yf.Ticker(stockName)

  #Call income statement class
  IncomeStatement = Income_Statement(ticker)
  
  
  historyPriceData = ticker.history(period="1mon",start = df["Start Date"],end = df["End Date"])

  st.write("#### Technical Chart - ",stockName)
  st.line_chart(historyPriceData.Close)

  st.session_state.ticker = ticker
  st.session_state.IncomeStatement = IncomeStatement

###INCOME STATEMENT PAGE
if menu == 'Income Statement':
   st.write("### Income Statement")   
   st.write(st.session_state.IncomeStatement.ShowIncomeStatement())



###BALANCE SHEET PAGE
if menu == 'Balance Sheet': 
   st.write("### Balance Sheet")
   


###CASH FLOW PAGE
if menu == 'Cash Flow':
   st.write("### Cash Flow")