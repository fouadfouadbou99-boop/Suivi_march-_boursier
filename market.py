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

    df.set_index(
        "Date",
        inplace=True
    )

    return df


def compute_metrics(df):

    close = df["Close"]

    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    close = close.dropna()

    current_year = close.index[-1].year

    ytd = close[
        close.index.year == current_year
    ]

    perf_ytd = (
        close.iloc[-1] /
        ytd.iloc[0] - 1
    ) * 100

    returns = close.pct_change().dropna()

    volatility = (
        returns.std()
        * np.sqrt(252)
        * 100
    )

    return {
        "Performance YTD (%)": round(perf_ytd, 2),
        "Volatilité (%)": round(volatility, 2)
    }
