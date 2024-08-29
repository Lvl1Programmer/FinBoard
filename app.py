import streamlit as st
import requests
import plotly.graph_objs as go
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')

# Sidebar inputs
st.sidebar.header("Input Options")
ticker = st.sidebar.text_input("Stock Ticker", value="AAPL")
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")

# Fetch stock data from Alpha Vantage
def fetch_stock_data(ticker, api_key):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=compact&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    # Check if 'Time Series (Daily)' is in the response
    if 'Time Series (Daily)' in data:
        return data['Time Series (Daily)']
    else:
        st.error("Failed to fetch data. Please check your API key, ticker symbol, and API limits.")
        return None

# Fetch financial ratios
def fetch_financial_ratios(ticker, api_key):
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={api_key}"
    response = requests.get(url)
    return response.json()

# Get the stock data and plot
data = fetch_stock_data(ticker, API_KEY)
if data:
    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.rename(columns={'4. close': 'Close'})  # Use '4. close' for the closing price
    df.index = pd.to_datetime(df.index)

    # Plot the stock price
    st.header(f"Stock Price for {ticker}")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close'))
    st.plotly_chart(fig)

    # Show financial ratios
    st.header(f"Financial Ratios for {ticker}")
    ratios = fetch_financial_ratios(ticker, API_KEY)
    st.write(ratios)
else:
    st.write("No data available for the selected ticker and API key.")

# Portfolio tracker placeholder
st.header("Portfolio Performance")
st.write("Portfolio tracking will go here")

# Running the app
if __name__ == "__main__":
    st.title("Financial Dashboard")