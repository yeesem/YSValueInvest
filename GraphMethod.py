import streamlit as st
import pandas as pd

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

class Graph:
    
    def __init__(self):
      pass
  
    def plot_annual_financial_graph(annual_data,col,numYear=0):
      annual_data[col] = annual_data[col].astype(float)
      
      fig, ax = plt.subplots(figsize=(35, 15))
      annual_data[col][numYear:].plot(ax=ax, color='brown')
      plt.xticks(rotation=45,fontsize=30)
      plt.ylabel(col,fontsize=35)
      plt.xlabel("Financial Year",fontsize = 35)
      ax.tick_params(axis='y', labelsize=30)
      ax.set_xticks(range(len(annual_data[col][numYear:])))
      ax.set_xticklabels(annual_data[col][numYear:].index,fontsize=30)
      # Annotate each point with its corresponding y-value
      for x, y in zip(range(len(annual_data[col][numYear:])), annual_data[col][numYear:]):
          plt.annotate(f'{y}', (x, y),fontsize=25,textcoords="offset points", xytext=(0, 5), ha='center', va='bottom', rotation=20)
      
      # Show plot using Streamlit
      st.pyplot(fig)
    