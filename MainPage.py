import yfinance as yf
import streamlit as st

import pandas as pd
import numpy as np
import datetime

import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from matplotlib.widgets import RectangleSelector
import mplcursors

import dash
from dash import Dash, html, Input, Output, dash_table
from dash.dependencies import Input,Output
import dash_core_components as dcc
import dash_html_components as html

from streamlit_option_menu import option_menu
from IncomeStatement import Income_Statement
from dateutil.relativedelta import relativedelta
from KLSEScraping import KLSE

###SIDEBAR
st.sidebar.header("Menu")
def menu():
      
      menu_option = st.sidebar.radio('Pages',
                               options = ["Main Page","Income Statement","Balance Sheet","Cash Flow","Shareholding Changes","Capital Changes"])
    
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
company_sector = stock_basic_info["company sector"]
company_website = stock_basic_info["company link"]

#@st.cache_data
def shareholding_changes_table():
    shareholding_changes_table = klse.shareholding_changes_table()
    return shareholding_changes_table

capital_changes_table = klse.capital_changes_table()

annual_financial_data = klse.get_annual_financial_data()

# Define the space between elements
space = "&nbsp;"

###MAIN PAGE
if menu == 'Main Page':
 
  #Method for timeline sidebar
  def timeline():
    
      st.sidebar.write("Date Range Selection")
      current_date =  datetime.datetime.now().date()
      start_date = current_date - datetime.timedelta(days = 10 * 365)
      initial_default_date = current_date - datetime.timedelta(days = 5 * 365)
      start = st.sidebar.slider("Start Date",start_date,current_date,value = initial_default_date)
      end = st.sidebar.slider("End Date",start_date,current_date,value = current_date)
    
      chartDate = {"Start Date":start,"End Date":end}
    
      return chartDate
  
  #Diaplay timeline side bar
  df = timeline()
  
  historyPriceData = ticker.history(period="1mon",start = df["Start Date"],end = df["End Date"])

  flex_style = "display: flex; justify-content: space-between;"

  # Determine the color based on the value of percentage_difference
  color = "green" if float(percentage_difference.strip('%')) > 0 else "red"

  st.write(f'<div style="{flex_style}; font-size: 35px;">'
         f'<span style="font-weight: bold;">'
         f'<a href = "{company_website}">{short_name} {symbol}</a>''</span>'
         f'<div style="text-align: right; font-size: 30px; color: {color};">'
         f'<span style="font-weight: bold;">{price} ({percentage_difference})</span>'
         f'</div></div>',
         unsafe_allow_html=True)
  
  st.write(
    f'<div style="margin-bottom: 5px;">'
    f'<span style="font-weight: bold; font-size: 25px;">{full_name}</span>'
    f'<br>'
    f'<span style="font-weight: bold; font-size: 20px;">{company_sector}</span>'
    f'</div>',
    unsafe_allow_html=True)
  
  st.markdown(stock_basic_info["company summary"])
  #st.write("\n")
  
  ## MAIN MANU - PLOT ANNUAL FINANCIAL DATA
  st.write(
  f'<div style="margin-bottom: 1px;">'
  f'<span style="font-weight: bold; font-size: 20px;">{"Annual Financial Data"}</span>'
  f'</div>',
  unsafe_allow_html=True)
    
  annual_data = annual_financial_data
  annual_data.index = annual_data.index.astype(str)
  
  annual_graph_option = st.radio(
    label = "Test",
    options = ("5Y","10Y","All"),
    index = 1,
    horizontal = True,
    label_visibility="collapsed"
  )
  
  if annual_graph_option == "All": 
      annual_data["EPS"] = annual_data["EPS"].astype(float)
      
      fig, ax = plt.subplots(figsize=(30, 10))
      annual_data["EPS"].plot(ax=ax, color='brown')
      plt.xticks(rotation=45)
      plt.ylabel("EPS")
      ax.set_xticks(range(len(annual_data)))
      ax.set_xticklabels(annual_data.index)
      # Annotate each point with its corresponding y-value
      for x, y in zip(range(len(annual_data)), annual_data["EPS"]):
          plt.annotate(f'{y}', (x, y), textcoords="offset points", xytext=(0, 5), ha='center', va='bottom', rotation=20)

      # Show plot using Streamlit
      st.pyplot(fig)
  
  elif annual_graph_option == "10Y":
      annual_data["EPS"] = annual_data["EPS"].astype(float)
      
      fig, ax = plt.subplots(figsize=(30, 10))
      annual_data["EPS"][-10:].plot(ax=ax, color='brown')
      plt.xticks(rotation=45,fontsize=17)
      plt.ylabel("EPS",fontsize=20)
      plt.xlabel("Finacial Year",fontsize = 20)
      ax.set_yticklabels(annual_data["EPS"][-10:],fontsize=17)
      ax.set_xticks(range(len(annual_data["EPS"][-10:])))
      ax.set_xticklabels(annual_data["EPS"][-10:].index,fontsize=17)
      # Annotate each point with its corresponding y-value
      for x, y in zip(range(len(annual_data["EPS"][-10:])), annual_data["EPS"][-10:]):
          plt.annotate(f'{y}', (x, y),fontsize=20,textcoords="offset points", xytext=(0, 5), ha='center', va='bottom', rotation=20)

      # Show plot using Streamlit
      st.pyplot(fig)
      
  elif annual_graph_option == "5Y":
      annual_data["EPS"] = annual_data["EPS"].astype(float)
      
      fig, ax = plt.subplots(figsize=(30, 10))
      annual_data["EPS"][-5:].plot(ax=ax, color='brown')
      plt.xticks(rotation=45)
      plt.ylabel("EPS")
      ax.set_xticks(range(len(annual_data["EPS"][-5:])))
      ax.set_xticklabels(annual_data["EPS"][-5:].index)
      # Annotate each point with its corresponding y-value
      for x, y in zip(range(len(annual_data["EPS"][-5:])), annual_data["EPS"][-5:]):
          plt.annotate(f'{y}', (x, y), textcoords="offset points", xytext=(0, 5), ha='center', va='bottom', rotation=20)

      # Show plot using Streamlit
      st.pyplot(fig)
      
  ### MAIN MENU - ANNUAL FINANCIAL DATA

  annual_data = annual_data[-10:]
  annual_data = annual_data.T[:-2]
  fig = go.Figure(data=go.Table(
  header=dict(values= [""] + list( annual_data.columns),
              fill_color="#D7DBDD",
              align='center'),
  cells=dict(values=[annual_data.index] + [annual_data[col] for col in annual_data],
              fill_color="#F4F6F6",
              align="left",
              height = 40,
              )))

  fig.update_layout(margin = dict(l=0,r=0,b=0,t=2),
                    height = 250) 
  
  # Show the Plotly figure using st.write()
  st.write(fig)

  # MAIN MENU - Technical Chart
  st.write("#### Technical Chart - ", stockName)
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
   
   
###SHAREHOLDING CHANGE PAGE
if menu == 'Shareholding Changes':
  st.write("### Shareholding Changes")
  
  shareholding_changes_table = shareholding_changes_table()
  
  shareholding_changes_table.insert(0, 'Index', range(1, len(shareholding_changes_table) + 1))
  
  fig = go.Figure(data=go.Table(
    header=dict(values=list(shareholding_changes_table.columns),
                fill_color="#D7DBDD",
                align='center'),
    cells=dict(values=[shareholding_changes_table[col] for col in shareholding_changes_table],
               fill_color="#F4F6F6",
               align="left",
               )))
  
  fig.update_layout(margin = dict(l=0,r=0,b=30,t=10),
                    height = 600,
                    ) 
  
  #Showing the graph
  st.plotly_chart(fig)

###CAPITAL CHANGE PAGE
if menu == 'Capital Changes':
  st.write("### Capital Changes")
  
  capital_changes_table.insert(0, 'Index', range(1, len(capital_changes_table) + 1))
  
  fig = go.Figure(data=go.Table(
    header=dict(values=list(capital_changes_table.columns),
                fill_color="#D7DBDD",
                align='center'),
    cells=dict(values=[capital_changes_table[col] for col in capital_changes_table],
               fill_color="#F4F6F6",
               align="left",
               height = 50
               )))
  
  fig.update_layout(margin = dict(l=0,r=0,b=30,t=10),
                    height = 600,
                    ) 
  
  st.plotly_chart(fig)
  