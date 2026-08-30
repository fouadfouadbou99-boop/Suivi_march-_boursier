import pandas as pd
import numpy as np
import yfinance as yf


def load_yahoo_data(symbol):

    df = yf.download(
        symbol,
        start="2020-01-01",
        auto_adjust=True,
        progress=False
    )

    return df


def load_maroc_index(filepath):

    df = pd.read_excel(filepath)

    df["Date"] = pd.to_datetime(df["Date"])

    df = df.sort_values("Date")

    df.set_index("Date", inplace=True)

    return df


def compute_metrics(df):

    close = df["Close"].dropna()

    current_year = close.index[-1].year

    ytd_data = close[
        close.index.year == current_year
    ]

    perf_ytd = (
        close.iloc[-1] /
        ytd_data.iloc[0]
        - 1
    ) * 100

    if len(close) >= 5:

        perf_1m = (
            close.iloc[-1] /
            close.iloc[-5]
            - 1
        ) * 100

    else:

        perf_1m = 0

    if len(close) >= 13:

        perf_3m = (
            close.iloc[-1] /
            close.iloc[-13]
            - 1
        ) * 100

    else:

        perf_3m = 0

    returns = close.pct_change().dropna()

    volatility = (
        returns.std()
        * np.sqrt(52)
        * 100
    )

    max_close = close.cummax()

    drawdown = (
        (close - max_close)
        / max_close
    )

    max_drawdown = (
        drawdown.min() * 100
    )

    return {

        "Performance 1 mois (%)":
        round(perf_1m, 2),

        "Performance 3 mois (%)":
        round(perf_3m, 2),

        "Performance YTD (%)":
        round(perf_ytd, 2),

        "Volatilité (%)":
        round(volatility, 2),

        "Drawdown 
