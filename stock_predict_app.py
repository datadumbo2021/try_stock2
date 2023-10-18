import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

st.title('반도체 주식 데이터 Dashboard')

tickers = {'SK hynix': '000660.KS', 'Samsung Electronics': '005930.KS', 'NVIDIA Corporation': 'NVDA', 'QUALCOMM': 'QCOM'}

selected_tickers = st.multiselect('Select the ticker symbols you want to visualize:', list(tickers.keys()))

start_date = st.date_input('Start Date', pd.to_datetime('2019-01-01'))
end_date = st.date_input('End Date', pd.to_datetime('today'))

def get_image_download_link(img, filename, text):
    buffered = BytesIO()
    img.savefig(buffered, format="png")
    img_data = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a download="{filename}" href="data:image/png;base64,{img_data}">{text}</a>'
    return href

if selected_tickers:
    for ticker in selected_tickers:
        data = yf.download(tickers[ticker], start=start_date, end=end_date)
        st.write(f"### {ticker} - Adjusted Close Price")
        st.line_chart(data['Adj Close'])

        fig, ax = plt.subplots()
        ax.plot(data.index, data['Adj Close'])
        ax.set_title(f'{ticker} Adjusted Close Price')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        
        st.markdown(get_image_download_link(fig, f"{ticker.replace(' ', '_')}_adjusted_close.png", 'Download Image'), unsafe_allow_html=True)
