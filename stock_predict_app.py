


import streamlit as st
import yfinance as yf
import pandas as pd
import base64
import matplotlib.pyplot as plt

st.title('반도체 주식 데이터 Dashboard')

tickers = {'SK hynix':'000660.KS', 'Samsung Electronics':'005930.KS', 'NVIDIA Corporation':'NVDA', 'QUALCOMM':'QCOM'}

reversed_ticker = dict(map(reversed, tickers.items()))

dropdown = st.multiselect('select', tickers.keys())

start = st.date_input('Start', value=pd.to_datetime('2019-01-01'))
end = st.date_input('End', value=pd.to_datetime('today'))

if len(dropdown) > 0:
    for i in dropdown:
        df = yf.download(tickers[i], start, end)['Adj Close']

        st.title(reversed_ticker[tickers[i]])
        st.line_chart(df)

        # 이미지로 저장
        plt.figure(figsize=(10,6))
        plt.plot(df.index, df.values, label=reversed_ticker[tickers[i]])
        plt.title(reversed_ticker[tickers[i]])
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)

        # 이미지를 바이트 데이터로 변환
        from io import BytesIO
        buffer = BytesIO()
        plt.savefig(buffer, format="jpg")
        buffer.seek(0)

        # 바이트 데이터를 base64로 인코딩
        image_b64 = base64.b64encode(buffer.getvalue()).decode()

        # 다운로드 링크 생성
        href = f'<a download="{reversed_ticker[tickers[i]]}.jpg" href="data:image/jpg;base64,{image_b64}">Download {reversed_ticker[tickers[i]]} Chart as JPG</a>'
        st.markdown(href, unsafe_allow_html=True)
