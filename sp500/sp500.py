# importing the required libraries
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import yfinance as yf

st.title('S&P 500 App')         # title of the website

st.markdown("""
This app retrieves the list of the **S&P 500** (from Wikipedia) and its corresponding **stock closing price** (year-to-date)!
* **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
""")         # to add a small description of the app
st.sidebar.header('User Input Features')     # heading of the sidebar


@st.cache      # if data is loaded once then it will not load again.
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'   # url from which the data is collected.
    html = pd.read_html(url, header = 0)       
    df = html[0]            # it contains 2 graphs and we will select only the first.
    return df

df = load_data()
sector = df.groupby('GICS Sector')          # based on the sector, grouping of data is done.

# Sidebar - Sector selection
sorted_sector_unique = sorted( df['GICS Sector'].unique() )        # to view only selected.
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique, sorted_sector_unique)  # to view all the sectors available.

# Filtering data
df_selected_sector = df[ (df['GICS Sector'].isin(selected_sector)) ]

st.header('Displaying Companies in Selected Sector')
st.write('Data Dimension: ' + str(df_selected_sector.shape[0]) + ' rows and ' + str(df_selected_sector.shape[1]) + ' columns.')  # 0 for row and 1 for column.
st.dataframe(df_selected_sector)

# to download the following data in a csv file format :
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)   # to download the file.

# what all datas that to be from the data set to plot the data

data = yf.download(
        tickers = list(df_selected_sector[:10].Symbol),
        period = "ytd",
        interval = "1d",
        group_by = 'ticker',
        auto_adjust = True,
        prepost = True,
        threads = True,
        proxy = None
    )

# Plot Closing Price of Query Symbol
def price_plot(symbol):
  df = pd.DataFrame(data[symbol].Close)
  df['Date'] = df.index
  plt.fill_between(df.Date, df.Close, color='skyblue', alpha=0.3)   # to fill under the curve
  plt.plot(df.Date, df.Close, color='skyblue', alpha=0.8)
  plt.xticks(rotation=90)
  plt.title(symbol, fontweight='bold')   # labeling and heading of the graph.
  plt.xlabel('Date', fontweight='bold')
  plt.ylabel('Closing Price', fontweight='bold')
  return st.pyplot()

num_company = st.sidebar.slider('Number of Companies', 1, 5)   # to create the sidebar for no. of companies to search.

if st.button('Show Plots'):         
    st.header('Stock Closing Price')
    for i in list(df_selected_sector.Symbol)[:num_company]:    # to print all the graph for number of companies selected.
        price_plot(i)