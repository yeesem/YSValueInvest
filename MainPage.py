import yfinance as yf
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from IncomeStatement import Income_Statement
from KLSEScraping import KLSE


###SIDEBAR
st.sidebar.header("Menu")
def menu():
      
      menu_option = st.sidebar.radio('Pages',
                               options = ["Main Page","Income Statement","Balance Sheet","Cash Flow"])
    
      return menu_option

menu = menu()

#User input stock symbol
key_stock_symbol = "1155"
stockName = st.text_input("Stock Symbol",key = key_stock_symbol,value = key_stock_symbol)
ticker = yf.Ticker(stockName + ".KL")

#Call income statement class
IncomeStatement = Income_Statement(ticker)
  
#Call KLSEScraping class
klse = KLSE(stockName)
stock_basic_info = klse.get_stock_basic_info()

short_name = stock_basic_info["short name"]
symbol = stock_basic_info["symbol"]
price = stock_basic_info["price"]
percentage_difference = stock_basic_info["different price in percentage"]
full_name = stock_basic_info["full name"]

# Define the space between elements
space = "&nbsp;" * 10

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
  
  historyPriceData = ticker.history(period="1mon",start = df["Start Date"],end = df["End Date"])

  flex_style = "display: flex; justify-content: space-between;"

  # Determine the color based on the value of percentage_difference
  color = "green" if float(percentage_difference.strip('%')) > 0 else "red"

  st.write(f'<div style="{flex_style}; font-size: 35px;">'
         f'<span style="font-weight: bold;">{short_name} {symbol}</span>'
         f'<div style="text-align: right; font-size: 30px; color: {color};">'
         f'<span style="font-weight: bold;">{price} ({percentage_difference})</span>'
         f'</div></div>',
         unsafe_allow_html=True)

  st.write("### " + full_name)

  st.markdown(stock_basic_info["company summary"])


  st.write("#### Technical Chart - ",stockName)
  st.line_chart(historyPriceData.Close)

  st.session_state.ticker = ticker
  st.session_state.IncomeStatement = IncomeStatement

###INCOME STATEMENT PAGE
if menu == 'Income Statement':
   flex_style = "display: flex; justify-content: space-between;"
   st.write(f'<div style="{flex_style}; font-size: 35px;">'
           f'<span style="font-weight: bold;">{full_name}</span>'
           f'</div>',
         unsafe_allow_html=True)
   st.write("### Income Statement")   
   st.write(st.session_state.IncomeStatement.ShowIncomeStatement())



###BALANCE SHEET PAGE
if menu == 'Balance Sheet': 
   st.write("### Balance Sheet")
   


###CASH FLOW PAGE
if menu == 'Cash Flow':
   st.write("### Cash Flow")