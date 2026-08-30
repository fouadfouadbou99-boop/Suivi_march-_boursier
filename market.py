import yfinance as yf
import pandas as pd
import numpy as np


def load_data(symbol, start="2020-01-01"):

    df = yf.download(
        symbol,
        start=start,
        auto_adjust=True,
        progress=False
    )

    return df


def compute_metrics(df):

    if df.empty:
        return {
            "Perf_YTD": 0.0,
            "Volatilite": 0.0
        }

    close = df["Close"]

    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    close = close.dropna()

    current_year = close.index[-1].year

    ytd_data = close[
        close.index.year == current_year
    ]

    perf_ytd = (
        float(close.iloc[-1]) /
        float(ytd_data.iloc[0])
    ) - 1

    returns = close.pct_change().dropna()

    volatility = float(
        returns.std() * np.sqrt(252)
    )

    return {
        "Perf_YTD": perf_ytd,
        "Volatilite": volatility
    }


def generate_commentary(symbol, metrics):

    return (
        f"Indice : {symbol}\n"
        f"Performance YTD : {metrics['Perf_YTD']:.2%}\n"
        f"Volatilité : {metrics['Volatilite']:.2%}"
    )
``
