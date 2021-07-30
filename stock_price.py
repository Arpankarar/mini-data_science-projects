import yfinance as yf
import streamlit as st
tickerSymbol = 'GOOGL'        #code of the company
st.write("""
# Simple Stock Price App                 
Shown are the stock **closing price** and ***volume*** of 
""" + tickerSymbol + """ !""")    # 2 star for bold and 3 star for italic bold


#get data on this ticker
tickerData = yf.Ticker(tickerSymbol)
#get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start='2010-5-31')  # starting and closing date


st.write("""
## Closing Price
""")                # h2 type heading 
st.line_chart(tickerDf.Close)            # to view the chart
st.write("""
## Volume Price      
""")              # h2 type heading 
st.line_chart(tickerDf.Volume)       # to view the chart